# DBot Agent Guide

This repo is an active bot/automation repo. Keep bot code and runtime setup here, and keep personal knowledge or interview notes in `../jobsearchautomation`.

Workspace control entrypoint: `/Users/sridharmuttumu/Documents/samples/WORKSPACE_INDEX.md`.

## AI Start Here

1. Use this repo for Discord bot code and runtime setup.
2. Treat `.env` as sensitive; never print or commit tokens.
3. Use `requirements.txt` for dependency changes.
4. Extract reusable AI/bot lessons to `../jobsearchautomation/learning` only when requested.

## Common Requests

- "Fix the bot": inspect the relevant entrypoint, then run `python -m py_compile` on changed Python files.
- "Update setup docs": edit README without exposing real tokens.
- "Add a new bot behavior": keep the change small, testable, and documented.

## Boundaries

- Bot source files and requirements stay in this repo.
- Do not print, copy, or commit secrets from `.env`.
- Do not move this repo into the personal knowledge hub; it is a separate product/tool repo.

## Project Shape

- `cxobot.py`: primary bot entry point or example branch focus.
- `discord_only.py` and `mybot.py`: alternate bot entry points or experiments.
- `requirements.txt`: Python dependencies.

## Working Rules

- Check `git status --short --branch` before edits.
- Treat `.env` as sensitive even if it is present locally.
- Prefer small, testable bot changes.
- Keep setup changes documented in `README.md`.
- Keep commits focused on this repo and push the active branch when requested.

## Verification

- For Python edits, run `python -m py_compile` on changed files.
- For dependency changes, update `requirements.txt` intentionally and note the runtime impact.
- Do not run networked bot actions unless the user asks.
