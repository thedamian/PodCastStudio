# Copyright (c) Microsoft. All rights reserved.
"""LM Studio-based web search agent for Agent Framework Debug UI.

This agent uses an LM Studio local server (OpenAI-compatible API) for chat
completions, combined with Ollama's hosted web search API as a tool.
"""

import os
import asyncio
from typing import Annotated
from datetime import datetime, timezone
from random import randint
from dotenv import load_dotenv

from agent_framework.openai import OpenAIChatClient
from pydantic import Field

load_dotenv()

def web_search(
    query: Annotated[str, Field(description="Search query")],
) -> str:
    """Perform web search using Ollama API."""
    import requests
    
    api_key = os.getenv("OLLAMA_API_KEY")
    if not api_key:
        return "Error: OLLAMA_API_KEY environment variable not set"
    
    url = "https://ollama.com/api/web_search"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "query": query
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        print(response.text)
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error fetching web content: {str(e)}"


def setup_agent():
    """Setup the LM Studio-based web search agent."""
    # Create an OpenAI-compatible chat client pointed at the LM Studio
    # local server. LM Studio exposes the OpenAI API at http://<host>:1234/v1.
    base_url = os.getenv("OPENAI_BASE_URL", "http://127.0.0.1:1234/v1")
    model_id = os.getenv("OPENAI_MODEL")
    # LM Studio does not require a real key, but the OpenAI SDK insists on
    # a non-empty string.
    api_key = os.getenv("OPENAI_API_KEY", "lm-studio")

    client = OpenAIChatClient(
        model=model_id,
        base_url=base_url,
        api_key=api_key,
    )

    # Agent instance following Agent Framework conventions
    agent = client.as_agent(
        name="SearchAgent",
        instructions="You are my assistant. Answer the questions based on the search engine.",
        tools=[web_search],
    )

    return agent

def main():
    """Launch the Ollama web search agent in DevUI."""
    import logging
    from agent_framework.devui import serve

    # Setup logging
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    logger = logging.getLogger(__name__)
    

    logger.info("Starting LM Studio Web Search Agent")
    logger.info("Available at: http://localhost:8090")
    logger.info("Entity ID: SearchAgent")
    logger.info(
        "Note: Make sure LM Studio's local server is running and that "
        "OPENAI_BASE_URL, OPENAI_MODEL (and OLLAMA_API_KEY for the "
        "web_search tool) are set in environment variables"
    )

    # Setup agent
    agent = setup_agent()

    # Launch server with the agent
    serve(entities=[agent], port=8090, auto_open=True, instrumentation_enabled=True)

if __name__ == "__main__":
    main()
