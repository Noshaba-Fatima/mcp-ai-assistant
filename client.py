
import asyncio
import os
import json
from pathlib import Path

from fastmcp import Client
from groq import Groq
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

# Initialize Groq
groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

MODEL = "openai/gpt-oss-120b"

SERVER_PATH = Path(__file__).with_name("main.py")


# Convert MCP tools into Groq-compatible definitions
def convert_mcp_tools_to_groq(mcp_tools):

    groq_tools = []

    for tool in mcp_tools:

        groq_tool = {
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description or "",
                "parameters": tool.input_schema
            }
        }

        groq_tools.append(groq_tool)

    return groq_tools


# Main client workflow

async def main():

    async with Client(SERVER_PATH) as client:

        # 1. Discover available MCP tools
        tools = await client.list_tools()

        print("Connected to MCP Server!")
        print("\nAvailable Tools:")

        for tool in tools:
            print(f"- {tool.name}: {tool.description}")

        # 2. Convert MCP tools into Groq format
        groq_tools = convert_mcp_tools_to_groq(tools)

        # 3. Get user query
        user_query = input("\nAsk me anything: ")

        messages = [
            {
                "role": "system",
                "content": (
                    "You are an assistant that can use available MCP tools. "
                    "Use the appropriate tool whenever necessary."
                )
            },
            {
                "role": "user",
                "content": user_query
            }
        ]

        # 4. Ask Groq to select a tool
        response = groq_client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=groq_tools,
            tool_choice="auto"
        )

        assistant_message = response.choices[0].message

        # 5. Execute the selected MCP tool
        if assistant_message.tool_calls:

            # Add Groq's tool-call message to conversation history
            messages.append(
                assistant_message.model_dump(exclude_none=True)
            )

            for tool_call in assistant_message.tool_calls:

                tool_name = tool_call.function.name

                arguments = json.loads(
                    tool_call.function.arguments
                )

                print(f"\nGroq selected: {tool_name}")
                print("Arguments:", arguments)

                print("\nExecuting MCP tool...")

                result = await client.call_tool(
                    tool_name,
                    arguments
                )

                print("MCP Result:", result.data)

                # 6. Send MCP result back to Groq
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(
                        result.data,
                        default=str
                    )
                })

            # 7. Ask Groq to generate the final response
            final_response = groq_client.chat.completions.create(
                model=MODEL,
                messages=messages
            )

            print("\nFinal AI Response:")
            print(final_response.choices[0].message.content)

        else:
            print("\nGroq Response:")
            print(assistant_message.content)


if __name__ == "__main__":
    asyncio.run(main())
