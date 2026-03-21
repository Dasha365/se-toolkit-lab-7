"""Command handlers - plain functions that return strings.

These handlers don't depend on Telegram. They can be called from:
- --test mode (CLI)
- Unit tests
- Telegram bot (when we add aiogram integration)
"""


def start() -> str:
    """Handle /start command."""
    return "Welcome to the LMS Bot! Use /help to see available commands."


def help() -> str:
    """Handle /help command."""
    return (
        "Available commands:\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/health - Check bot and LMS connection status\n"
        "/labs - List available labs\n"
        "/scores <lab> - Get scores for a specific lab"
    )


def health() -> str:
    """Handle /health command."""
    # TODO: Actually check LMS API connection
    return "Bot is running. LMS API status: not implemented yet."


def labs() -> str:
    """Handle /labs command."""
    # TODO: Fetch labs from LMS API
    return "Available labs: not implemented yet."


def scores(lab: str | None = None) -> str:
    """Handle /scores command.
    
    Args:
        lab: Optional lab identifier. If None, shows all scores.
    """
    # TODO: Fetch scores from LMS API
    if lab:
        return f"Scores for lab '{lab}': not implemented yet."
    return "Your scores: not implemented yet."
