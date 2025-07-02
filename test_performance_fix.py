#!/usr/bin/env python3
"""
Test the performance improvement with disable_tools option.
"""
from openai import OpenAI
import time

# Configure client to use local server
client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="dummy"  # or your API key if configured
)

print("Testing OpenAI API performance with and without tools...")

# Test 1: WITH tools (original behavior - slow)
print("\n=== Test 1: WITH tools (will be slow) ===")
start_time = time.time()

try:
    response = client.chat.completions.create(
        model="claude-3-5-sonnet-20241022",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "How does an OpenAI compatible API work?"}
        ],
        timeout=120  # 2 minute timeout
    )
    
    elapsed = time.time() - start_time
    print(f"✅ Response received in {elapsed:.2f} seconds")
    print(f"Response preview: {response.choices[0].message.content[:200]}...")
    print(f"Total tokens: {response.usage.total_tokens}")
    
except Exception as e:
    elapsed = time.time() - start_time
    print(f"❌ Request failed after {elapsed:.2f} seconds: {e}")

# Test 2: WITHOUT tools (new feature - fast)
print("\n=== Test 2: WITHOUT tools (should be fast) ===")
start_time = time.time()

try:
    response = client.chat.completions.create(
        model="claude-3-5-sonnet-20241022",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "How does an OpenAI compatible API work?"}
        ],
        extra_body={"disable_tools": True},  # NEW: Disable tools for faster response
        timeout=30  # 30 second timeout should be plenty
    )
    
    elapsed = time.time() - start_time
    print(f"✅ Response received in {elapsed:.2f} seconds")
    print(f"Response preview: {response.choices[0].message.content[:200]}...")
    print(f"Total tokens: {response.usage.total_tokens}")
    
except Exception as e:
    elapsed = time.time() - start_time
    print(f"❌ Request failed after {elapsed:.2f} seconds: {e}")

print("\n=== Performance Comparison ===")
print("With tools: Slow (reads codebase, uses tools)")
print("Without tools: Fast (direct Q&A response)")
print("\nTo use the fast mode, add: extra_body={'disable_tools': True}")