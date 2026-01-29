from __future__ import annotations
from flask import Flask
from threading import Thread
import os

app = Flask(__name__)

@app.route('/')
def home() -> str:
    # TODO: Return a simple status message indicating the bot is alive.
    return "Bot is running!"

def run() -> None:
    # TODO: Get PORT from environment variables, default to 8080.
    port = int(os.getenv("PORT", 8080))
    # TODO: Run Flask server on all interfaces (0.0.0.0)
    app.run(host='0.0.0.0', port=port, debug=False)

def keep_alive() -> None:
    # TODO: Start the Flask server in a separate daemon thread to avoid blocking the main bot thread.
    t = Thread(target=run)
    t.daemon = True
    t.start()