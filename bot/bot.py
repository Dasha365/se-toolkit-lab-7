"""Telegram LMS Bot entry point.

Usage:
    uv run bot.py --test "/start"   # Test a command without Telegram
    uv run bot.py                   # Run the actual Telegram bot
"""

import asyncio
import sys

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandStart

from config import settings
from handlers.commands import start, help, health, labs, scores


def run_test_mode(command: str) -> None:
    """Run a command in test mode - calls handler directly, prints result.

    Args:
        command: The command to test, e.g. "/start" or "/scores lab1"
    """
    # Strip leading slash and parse arguments
    parts = command.lstrip("/").split()
    cmd_name = parts[0]
    cmd_args = parts[1:] if len(parts) > 1 else []

    # Map command names to handler functions
    handlers = {
        "start": start,
        "help": help,
        "health": health,
        "labs": labs,
        "scores": scores,
    }

    if cmd_name not in handlers:
        print(f"Unknown command: /{cmd_name}")
        print(f"Available commands: {', '.join('/' + name for name in handlers)}")
        sys.exit(0)

    # Call the handler and print the result
    handler = handlers[cmd_name]
    if asyncio.iscoroutinefunction(handler):
        if cmd_args:
            result = asyncio.run(handler(*cmd_args))
        else:
            result = asyncio.run(handler())
    else:
        if cmd_args:
            result = handler(*cmd_args)
        else:
            result = handler()

    print(result)
    sys.exit(0)


async def cmd_start(message: types.Message) -> None:
    """Handle /start command."""
    await message.answer(start())


async def cmd_help(message: types.Message) -> None:
    """Handle /help command."""
    await message.answer(help())


async def cmd_health(message: types.Message) -> None:
    """Handle /health command."""
    result = await health()
    await message.answer(result)


async def cmd_labs(message: types.Message) -> None:
    """Handle /labs command."""
    result = await labs()
    await message.answer(result)


async def cmd_scores(message: types.Message) -> None:
    """Handle /scores command."""
    # Extract lab argument if provided
    lab = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else None
    result = await scores(lab)
    await message.answer(result)


async def run_telegram_bot() -> None:
    """Run the Telegram bot with aiogram."""
    if not settings.BOT_TOKEN:
        print("Error: BOT_TOKEN not set in .env.bot.secret")
        sys.exit(1)

    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()

    # Register command handlers
    dp.message.register(cmd_start, CommandStart())
    dp.message.register(cmd_start, Command("start"))
    dp.message.register(cmd_help, Command("help"))
    dp.message.register(cmd_health, Command("health"))
    dp.message.register(cmd_labs, Command("labs"))
    dp.message.register(cmd_scores, Command("scores"))

    print("Bot is starting...")
    await dp.start_polling(bot)


def main() -> None:
    """Main entry point."""
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        if len(sys.argv) < 3:
            print("Usage: uv run bot.py --test \"/command [args]\"")
            print("Example: uv run bot.py --test \"/start\"")
            sys.exit(1)

        command = sys.argv[2]
        run_test_mode(command)
    else:
        # Run the Telegram bot
        asyncio.run(run_telegram_bot())


if __name__ == "__main__":
    main()
