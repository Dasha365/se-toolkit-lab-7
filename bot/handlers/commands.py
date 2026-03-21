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

    # Count only labs
    labs = [item for item in items if item.get("type") == "lab"]
    count = len(labs) if labs else len(items)
    return f"Bot is running. LMS API: connected ({count} labs available)."


async def labs() -> str:
    """Handle /labs command."""
    client = LMSClient()
    items = await client.get_items()

    if isinstance(items, str):
        return f"Error fetching labs: {items}"

    if not items:
        return "No labs available."

    # Filter by type="lab" and get titles
    labs = [item for item in items if item.get("type") == "lab"]
    if not labs:
        return "No labs found."

    lab_titles = [item.get("title", item.get("name", item.get("id", "Unknown"))) for item in labs]
    return "Available labs:\n" + "\n".join(f"- {title}" for title in lab_titles)


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

        # Format pass rates as list of tasks with percentages
        if isinstance(rates, list):
            lines = [f"Scores for '{lab}':"]
            for task_data in rates:
                task_name = task_data.get("task", "Unknown task")
                avg_score = task_data.get("avg_score", 0)
                attempts = task_data.get("attempts", 0)
                lines.append(f"  • {task_name}: {avg_score:.1f}% ({attempts} attempts)")
            return "\n".join(lines)
        elif isinstance(rates, dict):
            lines = [f"Scores for '{lab}':"]
            for key, value in rates.items():
                if isinstance(value, float):
                    lines.append(f"  • {key}: {value:.1f}%")
                else:
                    lines.append(f"  • {key}: {value}")
            return "\n".join(lines)
        return f"Scores for '{lab}': {rates}"

    # Show all labs' scores
    items = await client.get_items()
    if isinstance(items, str):
        return f"Error fetching labs: {items}"

    # Filter by type="lab"
    labs = [item for item in items if item.get("type") == "lab"]
    if not labs:
        return "No labs found."

    results = ["Your scores:"]
    for item in labs:
        lab_id = str(item.get("id", "unknown"))
        lab_title = item.get("title", item.get("name", lab_id))
        rates = await client.get_pass_rates(lab_id)
        if isinstance(rates, str):
            results.append(f"  {lab_title}: error")
        elif isinstance(rates, list) and rates:
            # Calculate average across all tasks
            total_score = sum(t.get("avg_score", 0) for t in rates)
            avg = total_score / len(rates)
            results.append(f"  {lab_title}: {avg:.1f}% avg")
        elif isinstance(rates, dict):
            pass_rate = rates.get("pass_rate", rates.get("average_score", "N/A"))
            if isinstance(pass_rate, (int, float)):
                results.append(f"  {lab_title}: {pass_rate:.1f}%")
            else:
                results.append(f"  {lab_title}: {pass_rate}")
        else:
            results.append(f"  {lab_title}: N/A")

    return "\n".join(results)
