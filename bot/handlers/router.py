"""Intent router — routes natural language messages to backend tools via LLM.

Usage:
    from handlers.router import route

    answer = await route("Which lab has the lowest pass rate?")
"""

import sys

from services.lms_client import LMSClient
from services.llm_client import LLMClient


# Tool definitions — all 9 backend endpoints as LLM tool schemas
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_items",
            "description": "List all labs and tasks available in the LMS. Use this to discover what labs exist.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_learners",
            "description": "List all enrolled learners with their IDs and student groups. Use this to count total students or find group information.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_scores",
            "description": "Get score distribution histogram for a lab — shows how many students scored in each bucket (0-25, 26-50, 51-75, 76-100).",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {
                        "type": "string",
                        "description": "Lab identifier, e.g. 'lab-01', 'lab-02', 'lab-03'",
                    },
                },
                "required": ["lab"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_pass_rates",
            "description": "Get per-task average scores and attempt counts for a specific lab. Use this to compare task difficulty within a lab.",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {
                        "type": "string",
                        "description": "Lab identifier, e.g. 'lab-01', 'lab-02', 'lab-03'",
                    },
                },
                "required": ["lab"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_timeline",
            "description": "Get submission timeline — number of submissions per day for a lab. Use this to see when students were most active.",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {
                        "type": "string",
                        "description": "Lab identifier, e.g. 'lab-01', 'lab-02', 'lab-03'",
                    },
                },
                "required": ["lab"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_groups",
            "description": "Get per-group average scores and student counts for a lab. Use this to compare how different student groups performed.",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {
                        "type": "string",
                        "description": "Lab identifier, e.g. 'lab-01', 'lab-02', 'lab-03'",
                    },
                },
                "required": ["lab"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_top_learners",
            "description": "Get top N learners by average score for a lab, with their attempt counts. Use this to find the best performing students.",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {
                        "type": "string",
                        "description": "Lab identifier, e.g. 'lab-01', 'lab-02', 'lab-03'",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of top learners to return (default: 10)",
                    },
                },
                "required": ["lab"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_completion_rate",
            "description": "Get completion rate percentage for a lab — percentage of learners who scored >= 60. Includes passed and total counts.",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {
                        "type": "string",
                        "description": "Lab identifier, e.g. 'lab-01', 'lab-02', 'lab-03'",
                    },
                },
                "required": ["lab"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "trigger_sync",
            "description": "Trigger a data sync from the autochecker API to refresh all data. Use this when data might be stale.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
]


async def route(message: str) -> str:
    """Route a natural language message to backend tools via LLM.

    Args:
        message: The user's message (plain text).

    Returns:
        Final answer string from the LLM after tool execution.
    """
    llm = LLMClient()
    lms = LMSClient()

    try:
        response = await llm.chat(message, TOOLS, lms)
        return response
    except Exception as e:
        print(f"[error] LLM routing failed: {e}", file=sys.stderr)
        return "Sorry, I encountered an error processing your request. Please try again."
