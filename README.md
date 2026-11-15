# MCP AI Assistant

An AI-powered assistant built using the Model Context Protocol (MCP), FastMCP, Groq, and Streamlit.

This project demonstrates how Large Language Models (LLMs) can dynamically discover and execute tools exposed by a custom MCP server, enabling users to interact with external capabilities through natural-language conversations.

## Project Overview

The MCP AI Assistant follows a client-server architecture in which Groq acts as the reasoning engine and the MCP server exposes tools that the AI can invoke.

Users can submit queries in natural language. The assistant identifies the appropriate tool, executes it through the MCP client, and generates a human-readable response based on the execution result.

## Features

- **Custom MCP Server:** Developed using FastMCP to expose tools through the Model Context Protocol.
- **Custom MCP Client:** Connects to the MCP server and discovers available tools.
- **Dynamic Tool Discovery:** Retrieves tool definitions directly from the MCP server.
- **LLM Integration:** Uses Groq API for intelligent tool selection.
- **Automated Tool Execution:** Executes selected MCP tools based on LLM-generated tool calls.
- **Streamlit Interface:** Provides an interactive chat-based user interface.
- **Conversation Management:** Maintains conversation history during a session.

## Available MCP Tools

| Tool | Description |
|---|---|
| `calculate_compound_interest` | Calculates compound interest using principal, annual interest rate, and time period. |
| `get_server_status` | Checks the operational status of predefined services such as authentication, billing, and database. |

Additional tools will be introduced as the project evolves.

## System Architecture

```text
                    User
                     |
                     v
                Streamlit UI
                   app.py
                     |
                     v
              AI Agent / Backend
                  agent.py
                     |
                     v
                  Groq API
               (Tool Selection)
                     |
                     v
                 MCP Client
                    |
               STDIO Transport
                    |
                     v
                 MCP Server
                   main.py
                     |
              +------+------+
              |             |
              v             v
       Compound Interest  Service Status
          Calculator       Monitoring
```

## Project Structure

```text
my_mcp_server/
│
├── main.py              # Custom MCP server and tool definitions
├── client.py            # Standalone MCP client
├── agent.py             # Groq and MCP orchestration logic
├── app.py               # Streamlit application
│
├── .env                 # Environment variables (excluded from Git)
├── .gitignore
├── pyproject.toml       # Project dependencies and configuration
├── uv.lock              # Dependency lock file
└── README.md
```

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| FastMCP | MCP server and client implementation |
| Model Context Protocol | Standardized communication between AI applications and tools |
| Groq API | LLM inference and tool calling |
| Streamlit | Interactive application interface |
| uv | Python dependency and environment management |

## Prerequisites

Before running the project, ensure that you have:

- Python 3.14 or a compatible version
- uv package manager
- A Groq API key

## Installation and Setup

