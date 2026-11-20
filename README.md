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

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd my_mcp_server
```

### 2. Install Dependencies

```bash
uv sync
```

### 3. Configure Environment Variables

Create a `.env` file in the project root directory:

```env
GROQ_API_KEY=your_groq_api_key
```

Do not commit your `.env` file or expose your API key.

### 4. Run the MCP Server Inspector

```bash
uv run fastmcp dev inspector main.py
```

This allows you to inspect the MCP server and test its available tools.

### 5. Launch the Application

```bash
uv run streamlit run app.py
```

The Streamlit application will open in your browser.

## Example Queries

The assistant supports natural-language queries such as:

- Check whether the billing service is operational.
- Is the database service running?
- Calculate compound interest on 10000 at 5% for 3 years.

The assistant uses Groq to identify the appropriate MCP tool, executes it through the MCP client, and returns the result in natural language.

## Planned Enhancements

- [ ] Website availability monitoring
- [ ] System information and health monitoring
- [ ] File reading and search capabilities
- [ ] Additional mathematical and utility tools
- [ ] Improved tool execution logging
- [ ] Enhanced exception handling and validation
- [ ] Improved Streamlit interface
- [ ] MCP connection management
- [ ] Automated testing

## Project Objectives

The primary objective of this project is to explore how the Model Context Protocol enables LLMs to interact with external tools through a standardized interface.

The project focuses on implementing:

- MCP client-server communication
- Dynamic tool discovery
- LLM-driven tool selection
- Automated tool execution
- Integration of MCP with a conversational AI interface

## Author

**Noshaba Fatima**

---

This project is actively under development. Additional tools and capabilities will be introduced incrementally.
