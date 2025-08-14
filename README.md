# GServerBot

A simple Telegram bot built with Python and the `python-telegram-bot` library.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure the bot:**
   Create a `.env` file in the project root:
   ```
   TELEGRAM_BOT_TOKEN=your_actual_bot_token_here
   ```

## Usage

Run the bot:
```bash
python src/main.py
```

## Project Structure

```
GServerBot/
├── src/
│   ├── __init__.py
│   ├── main.py          # Main entry point
│   └── bot.py           # Bot implementation
├── tests/
├── requirements.txt      # Python dependencies
└── README.md
```

## Stopping the Bot

Press `Ctrl+C` in the terminal to stop the bot gracefully.

## Requirements

- Python 3.7+
- python-telegram-bot 20.7+
- python-dotenv 1.0.0+
