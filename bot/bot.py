"""Telegram LMS Bot entry point.

Usage:
    uv run bot.py --test "/start"   # Test a command without Telegram
    uv run bot.py                   # Run the actual Telegram bot
"""

import sys
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
        sys.exit(1)
    
    # Call the handler and print the result
    handler = handlers[cmd_name]
    if cmd_args:
        result = handler(*cmd_args)
    else:
        result = handler()
    
    print(result)
    sys.exit(0)


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
        # TODO: Run the actual Telegram bot with aiogram
        print("Running the Telegram bot (not implemented yet)")
        print("Use --test mode to test handlers: uv run bot.py --test \"/start\"")


if __name__ == "__main__":
    main()
