#!/usr/bin/env python3
"""
Test the exact user scenario to reproduce the hanging issue.
"""
import time
import asyncio
from claude_cli import ClaudeCodeCLI

async def test_user_scenario():
    """Test the exact scenario from the user's OpenAI client code."""
    print("Testing user scenario: How does an OpenAI compatible API work?")
    
    # Initialize CLI
    claude_cli = ClaudeCodeCLI(timeout=60000)  # 60 second timeout
    
    start_time = time.time()
    
    chunks = []
    try:
        async for chunk in claude_cli.run_completion(
            prompt="How does an OpenAI compatible API work?",
            system_prompt="You are a helpful assistant.",
            model="claude-3-5-sonnet-20241022",
            max_turns=10,  # Allow multiple turns for tool usage
            stream=False
        ):
            chunks.append(chunk)
            elapsed = time.time() - start_time
            print(f"[{elapsed:.1f}s] Chunk: {type(chunk).__name__ if hasattr(chunk, '__dict__') else type(chunk)}")
            
            # Print partial results to see progress
            if isinstance(chunk, dict):
                if 'content' in chunk:
                    print(f"  Content preview: {str(chunk['content'])[:100]}...")
                elif 'subtype' in chunk:
                    print(f"  Status: {chunk['subtype']}")
            
        elapsed = time.time() - start_time
        print(f"✅ Completed in {elapsed:.2f} seconds")
        print(f"Total chunks: {len(chunks)}")
        
        # Try to extract the final result
        result_chunk = None
        for chunk in reversed(chunks):
            if isinstance(chunk, dict) and chunk.get('subtype') in ['success', 'error_max_turns']:
                result_chunk = chunk
                break
        
        if result_chunk:
            print(f"Final status: {result_chunk.get('subtype')}")
            print(f"Cost: ${result_chunk.get('total_cost_usd', 0)}")
            print(f"Duration: {result_chunk.get('duration_ms', 0)}ms")
            
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"❌ Failed after {elapsed:.2f} seconds: {e}")

if __name__ == "__main__":
    asyncio.run(test_user_scenario())