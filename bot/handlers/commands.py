"""Command handlers - async functions that return strings.

These handlers fetch real data from the LMS API. They can be called from:
- --test mode (CLI)
- Unit tests
- Telegram bot (aiogram integration)
"""

import asyncio
from services.lms_client import LMSClient


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


async def health() -> str:
    """Handle /health command."""
    client = LMSClient()
    items = await client.get_items()

    if isinstance(items, str):
        return f"Bot is running. LMS API error: {items}"

    return f"Bot is running. LMS API: connected ({len(items)} items available)."


async def labs() -> str:
    """Handle /labs command."""
    client = LMSClient()
    items = await client.get_items()

    if isinstance(items, str):
        return f"Error fetching labs: {items}"

    if not items:
        return "No labs available."

    # Format lab list from items
    lab_names = [item.get("name", item.get("id", "Unknown")) for item in items]
    return "Available labs:\n" + "\n".join(f"- {name}" for name in lab_names)


async def scores(lab: str | None = None) -> str:
    """Handle /scores command.

    Args:
        lab: Optional lab identifier. If None, shows all scores.
    """
    client = LMSClient()

    if lab:
        rates = await client.get_pass_rates(lab)
        if isinstance(rates, str):
            return f"Error fetching scores for '{lab}': {rates}"

        # Format pass rates
        if isinstance(rates, dict):
            lines = [f"Pass rates for '{lab}':"]
            for key, value in rates.items():
                lines.append(f"  {key}: {value}")
            return "\n".join(lines)
        return f"Pass rates for '{lab}': {rates}"

    # Show all labs' scores
    items = await client.get_items()
    if isinstance(items, str):
        return f"Error fetching labs: {items}"

    if not items:
        return "No labs available."

    results = ["Your scores:"]
    for item in items:
        lab_id = item.get("id", "unknown")
        lab_name = item.get("name", lab_id)
        rates = await client.get_pass_rates(lab_id)
        if isinstance(rates, str):
            results.append(f"  {lab_name}: error")
        elif isinstance(rates, dict):
            pass_rate = rates.get("pass_rate", rates.get("average_score", "N/A"))
            results.append(f"  {lab_name}: {pass_rate}")
        else:
            results.append(f"  {lab_name}: N/A")

    return "\n".join(results)
