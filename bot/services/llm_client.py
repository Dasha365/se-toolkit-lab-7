"""LLM client with tool-calling support — OpenAI-compatible API.

Usage:
    from services.llm_client import LLMClient
    from services.lms_client import LMSClient

    llm = LLMClient()
    lms = LMSClient()

    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_items",
                "description": "List all labs and tasks",
                "parameters": {"type": "object", "properties": {}},
            },
        }
    ]

    response = await llm.chat("What labs are available?", tools, lms)
"""

import httpx
import sys
from config import settings


class LLMClient:
    """LLM client with tool-calling loop support.

    Sends user message + tool definitions to the LLM API.
    If LLM returns tool_calls, executes them via LMSClient,
    feeds results back, and repeats until final text response.
    """

    def __init__(self):
        self.api_base = settings.LLM_API_BASE_URL
        self.api_key = settings.LLM_API_KEY
        self.model = settings.LLM_API_MODEL
        self.timeout = 30.0  # seconds

    async def chat(self, user_message: str, tools: list, lms_client) -> str:
        """Chat with the LLM using tool-calling loop.

        Args:
            user_message: The user's message.
            tools: List of tool definitions (OpenAI format).
            lms_client: LMSClient instance to execute tool calls.

        Returns:
            Final text response from the LLM.
        """
        # Build conversation history with system prompt
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant for a university LMS. "
                    "You have access to tools that fetch data about labs, students, scores, and analytics. "
                    "When the user asks a question, use the available tools to get the data. "
                    "Always call tools when you need data — don't guess. "
                    "After receiving tool results, synthesize them into a clear, helpful answer. "
                    "If the user's message is unclear or ambiguous, ask for clarification. "
                    "If the user greets you, respond warmly and mention what you can help with."
                ),
            },
            {"role": "user", "content": user_message},
        ]

        # Tool-calling loop
        max_iterations = 5  # Prevent infinite loops
        iteration = 0

        async with httpx.AsyncClient(timeout=self.timeout) as http_client:
            while iteration < max_iterations:
                iteration += 1

                # Call the LLM
                response = await http_client.post(
                    f"{self.api_base}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": self.model,
                        "messages": messages,
                        "tools": tools,
                        "tool_choice": "auto",
                    },
                )
                response.raise_for_status()
                data = response.json()

                # Get the assistant message
                assistant_message = data["choices"][0]["message"]
                messages.append(assistant_message)

                # Check for tool calls
                tool_calls = assistant_message.get("tool_calls")

                if not tool_calls:
                    # No tool calls — return the final text response
                    return assistant_message.get("content", "")

                # Execute tool calls and collect results
                tool_results = []
                for tool_call in tool_calls:
                    function = tool_call["function"]
                    tool_name = function["name"]
                    tool_args = function.get("arguments", {})

                    # Parse arguments if they're a JSON string
                    if isinstance(tool_args, str):
                        import json
                        try:
                            tool_args = json.loads(tool_args)
                        except json.JSONDecodeError:
                            tool_args = {}

                    # Log the tool call to stderr for debugging
                    print(f"[tool] LLM called: {tool_name}({tool_args})", file=sys.stderr)

                    # Execute the tool via LMSClient
                    result = await self._execute_tool(tool_name, tool_args, lms_client)

                    # Log the result to stderr
                    if isinstance(result, (dict, list)):
                        result_summary = f"{len(result)} items" if isinstance(result, list) else f"{len(result)} keys"
                    else:
                        result_summary = str(result)[:100]
                    print(f"[tool] Result: {result_summary}", file=sys.stderr)

                    # Add tool result to conversation
                    tool_results.append({
                        "role": "tool",
                        "tool_call_id": tool_call["id"],
                        "content": str(result),
                    })

                # Feed tool results back to the LLM
                messages.extend(tool_results)
                print(f"[summary] Feeding {len(tool_results)} tool result(s) back to LLM", file=sys.stderr)

            # Max iterations reached
            return "I'm having trouble completing this request. Please try rephrasing your question."

    async def _execute_tool(self, name: str, args: dict, lms_client) -> any:
        """Execute a tool by calling the appropriate LMSClient method.

        Args:
            name: Tool name.
            args: Tool arguments.
            lms_client: LMSClient instance.

        Returns:
            Tool result (list, dict, or error string).
        """
        # Map tool names to LMSClient methods
        if name == "get_items":
            return await lms_client.get_items()
        elif name == "get_learners":
            return await lms_client.get_learners()
        elif name == "get_scores":
            lab = args.get("lab", "")
            return await lms_client.get_scores(lab)
        elif name == "get_pass_rates":
            lab = args.get("lab", "")
            return await lms_client.get_pass_rates(lab)
        elif name == "get_timeline":
            lab = args.get("lab", "")
            return await lms_client.get_timeline(lab)
        elif name == "get_groups":
            lab = args.get("lab", "")
            return await lms_client.get_groups(lab)
        elif name == "get_top_learners":
            lab = args.get("lab", "")
            limit = args.get("limit", 10)
            return await lms_client.get_top_learners(lab, limit)
        elif name == "get_completion_rate":
            lab = args.get("lab", "")
            return await lms_client.get_completion_rate(lab)
        elif name == "trigger_sync":
            return await lms_client.trigger_sync()
        else:
            return f"Unknown tool: {name}"
