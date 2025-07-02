#!/usr/bin/env python3
"""
Quick debug test to isolate the performance issue.
"""
import asyncio
import time
from claude_cli import ClaudeCodeCLI

async def test_wrapper_performance():
    """Test the wrapper performance directly."""
    print("Testing Claude Code wrapper performance...")
    
    # Initialize CLI
    claude_cli = ClaudeCodeCLI(timeout=30000)  # 30 second timeout
    
    # Test 1: Simple query without system prompt
    print("\n=== Test 1: Simple query (no system prompt) ===")
    start_time = time.time()
    
    chunks = []
    try:
        async for chunk in claude_cli.run_completion(
            prompt="What is 2 + 2?",
            model="claude-3-5-sonnet-20241022",
            max_turns=1,
            stream=False
        ):
            chunks.append(chunk)
            print(f"Chunk: {chunk}")
            
        elapsed = time.time() - start_time
        print(f"✅ Test 1 completed in {elapsed:.2f} seconds")
        print(f"Total chunks: {len(chunks)}")
        
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"❌ Test 1 failed after {elapsed:.2f} seconds: {e}")
    
    # Test 2: Query with system prompt
    print("\n=== Test 2: Query with system prompt ===")
    start_time = time.time()
    
    chunks = []
    try:
        async for chunk in claude_cli.run_completion(
            prompt="What files are in the current directory?",
            system_prompt="You are a helpful assistant.",
            model="claude-3-5-sonnet-20241022",
            max_turns=1,
            stream=False
        ):
            chunks.append(chunk)
            print(f"Chunk: {chunk}")
            
        elapsed = time.time() - start_time
        print(f"✅ Test 2 completed in {elapsed:.2f} seconds")
        print(f"Total chunks: {len(chunks)}")
        
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"❌ Test 2 failed after {elapsed:.2f} seconds: {e}")

if __name__ == "__main__":
    asyncio.run(test_wrapper_performance())