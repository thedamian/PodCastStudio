# Copyright (c) Microsoft. All rights reserved.
"""LM Studio-based script generation agent for Agent Framework Debug UI.

This agent uses an LM Studio local server (OpenAI-compatible API) for chat
completions.
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

def setup_gen_script_agent():
    """Setup the LM Studio-based script generation agent."""
    # Create an OpenAI-compatible chat client pointed at the LM Studio
    # local server. LM Studio exposes the OpenAI API at http://<host>:1234/v1.
    client = OpenAIChatClient(
        model=os.getenv("OPENAI_MODEL"),
        base_url=os.getenv("OPENAI_BASE_URL", "http://127.0.0.1:1234/v1"),
        api_key=os.getenv("OPENAI_API_KEY", "lm-studio"),
    )
    
    # Agent instance following Agent Framework conventions
    agent = client.as_agent(
        name="GenerateScriptAgent",
        instructions="""
        You are my English podcast script generation assistant. Please generate a 10-minute English podcast script based on the provided content.
        Note that the podcast is co-hosted by host Lucy and expert Ken. The script content is produced based on the input content, and the final output format is as follows:

            Speaker 1: ……
            Speaker 2: ……
            Speaker 1: ……
            Speaker 2: ……
            Speaker 1: ……
            Speaker 2: ……
        """
    )
    
    return agent

