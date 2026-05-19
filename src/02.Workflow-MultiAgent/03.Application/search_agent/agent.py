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


def setup_search_agent():
    """Setup the LM Studio-based web search agent."""
    # Create an OpenAI-compatible chat client pointed at the LM Studio
    # local server. LM Studio exposes the OpenAI API at http://<host>:1234/v1.
    client = OpenAIChatClient(
        model=os.getenv("OPENAI_MODEL"),
        base_url=os.getenv("OPENAI_BASE_URL", "http://127.0.0.1:1234/v1"),
        api_key=os.getenv("OPENAI_API_KEY", "lm-studio"),
    )

    # Agent instance following Agent Framework conventions
    agent = client.as_agent(
        name="SearchAgent",
        instructions="You are my assistant. Answer the questions based on the search engine.",
        tools=[web_search],
    )

    return agent
