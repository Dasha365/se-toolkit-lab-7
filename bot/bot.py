"""Telegram LMS Bot entry point.

Usage:
    uv run bot.py --test "/start"   # Test a command without Telegram
    uv run bot.py                   # Run the actual Telegram bot
"""

import asyncio
import inspect
import ssl
import sys

import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.filters import Command, CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import settings
from handlers.commands import start, help, health, labs, scores
from handlers.router import route


def run_test_mode(command: str) -> None:
    """Run a command or message in test mode - calls handler directly, prints result.

    Args:
        command: The command or message to test, e.g. "/start" or "which lab is hardest"
    """
    # Check if it's a command (starts with /)
    if command.startswith("/"):
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
        if inspect.iscoroutinefunction(handler):
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
    else:
        # Plain text message - use the LLM router
        result = asyncio.run(route(command))
        print(result)

    sys.exit(0)


async def cmd_start(message: types.Message) -> None:
    """Handle /start command with inline keyboard."""
    # Create inline keyboard with 4 buttons
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📋 Labs", callback_data="labs"),
                InlineKeyboardButton(text="🏥 Health Check", callback_data="health"),
            ],
            [
                InlineKeyboardButton(text="📊 Scores Lab 04", callback_data="scores"),
                InlineKeyboardButton(text="🏆 Top Students", callback_data="top_students"),
            ],
        ],
    )
    await message.answer(start(), reply_markup=keyboard)


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


async def handle_text_message(message: types.Message) -> None:
    """Handle plain text messages via LLM router."""
    result = await route(message.text)
    await message.answer(result)


async def handle_callback_query(callback_query: types.CallbackQuery) -> None:
    """Handle inline keyboard button clicks.
    
    Args:
        callback_query: The callback query from the button click
    """
    data = callback_query.data
    
    # Map callback data to handler functions
    handlers = {
        "labs": labs,
        "health": health,
        "scores": scores,
        "top_students": scores,  # Top students uses scores handler
    }
    
    if data not in handlers:
        await callback_query.answer("Unknown action", show_alert=True)
        return
    
    # Call the handler
    handler = handlers[data]
    if inspect.iscoroutinefunction(handler):
        result = await handler()
    else:
        result = handler()
    
    # Send the result as a new message
    await callback_query.message.answer(result)
    # Acknowledge the callback
    await callback_query.answer()


async def run_telegram_bot() -> None:
    """Run the Telegram bot with aiogram."""
    if not settings.BOT_TOKEN:
        print("Error: BOT_TOKEN not set in .env.bot.secret")
        sys.exit(1)

    # Create SSL context that disables verification
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    # Create connector with custom SSL context
    connector = aiohttp.TCPConnector(ssl=ssl_context)

    # Create session with connector factory
    session = AiohttpSession(connector=lambda: connector)

    bot = Bot(
        token=settings.BOT_TOKEN,
        session=session,
        default=DefaultBotProperties(parse_mode="HTML"),
    )
    dp = Dispatcher()

    # Register command handlers
    dp.message.register(cmd_start, CommandStart())
    dp.message.register(cmd_start, Command("start"))
    dp.message.register(cmd_help, Command("help"))
    dp.message.register(cmd_health, Command("health"))
    dp.message.register(cmd_labs, Command("labs"))
    dp.message.register(cmd_scores, Command("scores"))

    # Register plain text message handler (catches all non-command messages)
    dp.message.register(handle_text_message)

    # Register callback query handler for inline keyboard buttons
    dp.callback_query.register(handle_callback_query)

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
