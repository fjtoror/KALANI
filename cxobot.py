from dotenv import load_dotenv
from openai import OpenAI
import discord
import os

load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_KEY")
DISCORD_TOKEN = os.getenv("TOKEN")

openai_client = OpenAI(api_key=OPENAI_KEY)

# Conversation histories per user: list of {"role": "user"|"assistant", "content": "..."}
convo_histories = {}

MAX_USER_MESSAGES = 20

SYSTEM_PROMPT = (
    "You are a helpful, patient customer support agent for an online learning platform "
    "similar to Coursera. Answer user questions about enrollment, billing, certificates, "
    "course recommendations, technical troubleshooting, and account management. Be concise, "
    "polite, and show step-by-step troubleshooting when relevant. If you need more info, ask "
    "one clarifying question. Use plain language and avoid marketing fluff."
)


def ensure_history(user_id: str):
    if user_id not in convo_histories:
        convo_histories[user_id] = {"messages": [], "user_count": 0}


def trim_history(user_id: str):
    h = convo_histories[user_id]
    # Remove oldest messages until user_count <= MAX_USER_MESSAGES
    while h["user_count"] > MAX_USER_MESSAGES:
        if not h["messages"]:
            h["user_count"] = 0
            break
        removed = h["messages"].pop(0)
        if removed.get("role") == "user":
            h["user_count"] -= 1


def add_message(user_id: str, role: str, content: str):
    ensure_history(user_id)
    h = convo_histories[user_id]
    h["messages"].append({"role": role, "content": content})
    if role == "user":
        h["user_count"] += 1
    trim_history(user_id)


def build_chat_messages(user_id: str, user_input: str):
    ensure_history(user_id)
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(convo_histories[user_id]["messages"])
    messages.append({"role": "user", "content": user_input})
    return messages


def call_openai_chat(messages):
    completion = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=800,
    )
    return completion.choices[0].message.content


# Discord setup
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")


@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return

    is_dm = message.guild is None
    starts_support = message.content.strip().lower().startswith("!support")

    if not (is_dm or starts_support):
        return

    user_id = str(message.author.id)
    # Get user text (if channel, strip prefix)
    if is_dm:
        user_text = message.content.strip()
    else:
        # remove the command prefix
        user_text = message.content.strip()[len("!support") :].strip()
        if not user_text:
            await message.channel.send(
                "Please include your question after `!support`. Example: `!support I can't access my course.`"
            )
            return

    # Special commands
    cmd = user_text.lower()
    if cmd == "!history" or cmd == "history":
        ensure_history(user_id)
        msgs = convo_histories[user_id]["messages"]
        if not msgs:
            await message.channel.send("No conversation history found.")
            return
        summary = []
        for m in msgs[-20:]:
            prefix = "User: " if m["role"] == "user" else "Agent: "
            summary.append(prefix + m["content"])
        await message.channel.send("\n".join(summary))
        return

    if cmd == "!reset" or cmd == "reset":
        convo_histories.pop(user_id, None)
        await message.channel.send("Your conversation history has been cleared.")
        return

    # Normal support flow
    add_message(user_id, "user", user_text)
    chat_messages = build_chat_messages(user_id, user_text)

    try:
        response = call_openai_chat(chat_messages)
    except Exception as e:
        await message.channel.send("Sorry — I couldn't reach the support engine. Try again later.")
        return

    # Save assistant reply and reply on Discord
    add_message(user_id, "assistant", response)
    await message.channel.send(response)


if __name__ == "__main__":
    if not OPENAI_KEY or not DISCORD_TOKEN:
        print("Missing OPENAI_KEY or TOKEN in environment. Add them to .env.")
    else:
        client.run(DISCORD_TOKEN)
