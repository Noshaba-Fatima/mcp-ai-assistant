
import asyncio
import streamlit as st

from agent import process_query


# Page configuration
st.set_page_config(
    page_title="MCP AI Assistant",
    page_icon="🤖",
    layout="wide"
)


# Initialize session state
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = None

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

if "available_tools" not in st.session_state:
    st.session_state.available_tools = []


# Application header
st.title("🤖 MCP AI Assistant")

st.caption(
    "An AI assistant powered by Groq and Model Context Protocol."
)


# Sidebar
with st.sidebar:

    st.header("MCP Server")

    st.success("Server connection is managed automatically")

    st.subheader("Available Tools")

    if st.session_state.available_tools:

        for tool in st.session_state.available_tools:
            st.markdown(f"**{tool['name']}**")
            st.caption(tool["description"])

    else:
        st.info("Tools will appear after your first query.")

    if st.button("Clear Conversation"):

        st.session_state.conversation_history = None
        st.session_state.chat_messages = []
        st.rerun()


# Display previous messages
for message in st.session_state.chat_messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Chat input
user_query = st.chat_input("Ask me anything...")

if user_query:

    # Display user message
    st.session_state.chat_messages.append({
        "role": "user",
        "content": user_query
    })

    with st.chat_message("user"):
        st.markdown(user_query)

    # Process query using our MCP + Groq backend
    with st.chat_message("assistant"):

        with st.spinner("Thinking and executing MCP tools..."):

            try:

                answer, updated_history, tools = asyncio.run(
                    process_query(
                        user_query,
                        st.session_state.conversation_history
                    )
                )

                st.session_state.conversation_history = updated_history

                st.session_state.available_tools = [
                    {
                        "name": tool.name,
                        "description": tool.description or ""
                    }
                    for tool in tools
                ]

                st.markdown(answer)

                st.session_state.chat_messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as e:

                st.error(f"Something went wrong: {str(e)}")
