
import os
import json
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq
from fastmcp import Client


load_dotenv()

groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

MODEL = "openai/gpt-oss-120b"

SERVER_PATH = Path(__file__).with_name("main.py")


def convert_mcp_tools_to_groq(mcp_tools):

    groq_tools = []

    for tool in mcp_tools:

        groq_tools.append({
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description or "",
                "parameters": tool.input_schema
            }
        })

    return groq_tools


async def process_query(user_query, conversation_history=None):

    if conversation_history is None:
        conversation_history = [
            {
                "role": "system",
                "content": (
                    "You are a helpful AI assistant. "
                    "Use available MCP tools whenever appropriate."
                )
            }
        ]

    conversation_history.append({
        "role": "user",
        "content": user_query
    })

    async with Client(SERVER_PATH) as client:

        tools = await client.list_tools()

        groq_tools = convert_mcp_tools_to_groq(tools)

        tool_map = {tool.name: tool for tool in tools}

        response = groq_client.chat.completions.create(
            model=MODEL,
            messages=conversation_history,
            tools=groq_tools,
            tool_choice="auto"
        )

        assistant_message = response.choices[0].message

        if assistant_message.tool_calls:

            conversation_history.append(
                assistant_message.model_dump(exclude_none=True)
            )

            for tool_call in assistant_message.tool_calls:

                tool_name = tool_call.function.name

                if tool_name not in tool_map:
                    raise ValueError(f"Unknown MCP tool: {tool_name}")

                arguments = json.loads(
                    tool_call.function.arguments
                )

                result = await client.call_tool(
                    tool_name,
                    arguments
                )

                conversation_history.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result.data, default=str)
                })

            final_response = groq_client.chat.completions.create(
                model=MODEL,
                messages=conversation_history
            )

            answer = final_response.choices[0].message.content

        else:

            answer = assistant_message.content

        conversation_history.append({
            "role": "assistant",
            "content": answer
        })

        return answer, conversation_history, tools
