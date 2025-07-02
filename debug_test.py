#!/usr/bin/env python3
"""
Debug test to see what the Claude Code SDK is returning.
"""

import asyncio
import logging
from claude_cli import ClaudeCodeCLI

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Also enable logging for our modules
logging.getLogger('claude_cli').setLevel(logging.DEBUG)

async def test_sdk_directly():
    print("Testing Claude Code SDK directly...")
    
    cli = ClaudeCodeCLI()
    
    chunks = []
    async for chunk in cli.run_completion(
        prompt="Say 'Hello from SDK!' and nothing else.",
        model="claude-3-5-haiku-20241022",
        max_turns=1,
        stream=False
    ):
        print(f"Chunk type: {type(chunk)}")
        print(f"Chunk: {chunk}")
        chunks.append(chunk)
    
    print(f"\nTotal chunks received: {len(chunks)}")
    
    # Try to parse message
    assistant_content = cli.parse_claude_message(chunks)
    print(f"Parsed content: {assistant_content}")
    
    # Check metadata
    metadata = cli.extract_metadata(chunks)
    print(f"Metadata: {metadata}")

if __name__ == "__main__":
    asyncio.run(test_sdk_directly())