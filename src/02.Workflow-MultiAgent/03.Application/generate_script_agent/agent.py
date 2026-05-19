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
        You are an English podcast script generation assistant. Generate a 10-minute English podcast script based on the provided content.
        The podcast is co-hosted by Lucy (host) and Ken (expert).

        STRICT OUTPUT RULES — violation will break downstream text-to-speech:
        - Every line MUST start with exactly "Speaker 1:" or "Speaker 2:" (no asterisks, no bold, no markdown).
        - Speaker 1 is Lucy. Speaker 2 is Ken.
        - Do NOT include a title, episode header, duration, hosts line, or any metadata.
        - Do NOT include sound effect lines or stage directions.
        - Do NOT use any markdown formatting (no **, no *, no #, no italics).
        - Do NOT use special characters from other languages in the output (write foreign words in plain ASCII approximations if needed).
        - Output ONLY the alternating Speaker lines, nothing else.

        Correct format:
        Speaker 1: Hello and welcome back to Global Rhythms.
        Speaker 2: Thanks for having me. Today we are talking about Cuba.
        Speaker 1: That is right. Let us start with the music.
        """
    )
    
    return agent
