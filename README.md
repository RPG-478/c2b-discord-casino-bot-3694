# Discord Casino Bot (Python/discord.py)

## Overview
This is a modular, Cogs-based Discord bot designed to provide a comprehensive gambling and casino experience within a Discord server. It features a persistent economy system and various gambling games.

## Key Features
*   **Persistent Economy:** User balances, daily cooldowns, and statistics are stored persistently using JSON files (`data/user_data.json`).
*   **Core Commands:** Check balance (`/balance`), claim daily rewards (`/daily`).
*   **Gambling Games:** Includes complex games like Roulette, Slots (with image generation via Pillow), Blackjack, and Chinchiro.
*   **Ranking System:** Global leaderboard based on user wealth.
*   **Modular Architecture:** Uses Discord.py Cogs (`CasinoCore`, `Leaderboard`, `GamblingGames`) for clean separation of concerns.

## Architecture Summary
*   **Language:** Python 3.11+
*   **Framework:** discord.py (2.x+)
*   **Persistence:** JSON File Storage (`data/user_data.json`)
*   **Health Check:** Flask server (`keep_alive.py`)

## Setup and Installation

### 1. Prerequisites
*   Python 3.11+
*   Required libraries (install via `pip install -r requirements.txt`): `discord.py`, `Pillow`, `Flask`.

### 2. Configuration
Create a `.env` file based on `.env.example` and fill in your bot token.

### 3. Running the Bot
```bash
python main.py
```