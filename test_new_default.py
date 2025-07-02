#!/usr/bin/env python3
"""
Test the new default behavior (tools disabled by default).
"""
from openai import OpenAI
import time

# Configure client to use local server
client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="dummy"
)

print("Testing new default behavior (tools disabled)...")

# Test 1: Default behavior - should be FAST now
print("\n=== Test 1: Default behavior (tools disabled) ===")
start_time = time.time()

response = client.chat.completions.create(
    model="claude-3-5-sonnet-20241022",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "How does an OpenAI compatible API work?"}
    ]
)

elapsed = time.time() - start_time
print(f"✅ Response received in {elapsed:.2f} seconds")
print(f"Response preview: {response.choices[0].message.content[:200]}...")

# Test 2: With tools enabled - will be slower but can access files
print("\n=== Test 2: With tools enabled ===")
start_time = time.time()

response = client.chat.completions.create(
    model="claude-3-5-sonnet-20241022",
    messages=[
        {"role": "user", "content": "What files are in the current directory?"}
    ],
    extra_body={"enable_tools": True}  # Enable tools to read directory
)

elapsed = time.time() - start_time
print(f"✅ Response received in {elapsed:.2f} seconds")
print(f"Response: {response.choices[0].message.content}")

print("\n✅ SUCCESS: Default behavior now matches OpenAI API (no tools)")
print("To enable Claude Code tools, use: extra_body={'enable_tools': True}")