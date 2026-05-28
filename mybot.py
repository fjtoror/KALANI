from dotenv import load_dotenv
from openai import OpenAI
from google import genai
import discord
import os

# Load environment variables from .env file
load_dotenv()
OPENAI_KEY = os.getenv('OPENAI_KEY')
DISCORD_TOKEN = os.getenv('TOKEN')

# Initialize the OpenAI client
openai_client = OpenAI(api_key=OPENAI_KEY)

def call_openai(question):
    completion = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
             {
                 "role": "user",
                 "content": f"Respond like a monk to the following question:  {question}",
            },
        ]
    )
    # Print the response
    response = completion.choices[0].message.content
    print(response)
    return response

def call_gemini(question, history=None):

    client = genai.Client(api_key=os.getenv('GEMINI_KEY'))

    if history is None:
        history = []

    history.append({"role": "user", "parts": [{"text": f"Respond like a monk to the following question:  {question}"}]})

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=history
    )

    history.append({"role": "model", "parts": [{"text": response.text}]})

    print(response.text)
    return response.text




# Set up discord
intents = discord.Intents.default()
intents.message_content = True  
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$question'):
        print(f"Message: {message.content}")                
        message_content = message.content.split("$question")[1]
        print(f"Question: {message_content}")    
        response = call_openai(message_content)   
        print(f"Assistant: {response}")    
        print("---")
        await message.channel.send(response)

    if message.content.startswith('$g'):
        print(f"Message: {message.content}")                
        message_content = message.content.split("$g")[1]
        print(f"Question: {message_content}")    
        response = call_gemini(message_content)   
        print(f"Assistant: {response}")    
        print("---")
        await message.channel.send(response)

client.run(DISCORD_TOKEN)
