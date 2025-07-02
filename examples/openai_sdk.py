#!/usr/bin/env python3
"""
Claude Code OpenAI API Wrapper - OpenAI SDK Example

This example demonstrates how to use the OpenAI Python SDK
with the Claude Code wrapper.
"""

from openai import OpenAI
import os
from typing import Optional

# Configuration
BASE_URL = "http://localhost:8000/v1"
API_KEY = os.getenv("API_KEY", "dummy")  # Use "dummy" if no auth required


def create_client(base_url: str = BASE_URL, api_key: str = API_KEY) -> OpenAI:
    """Create OpenAI client configured for Claude Code wrapper."""
    return OpenAI(
        base_url=base_url,
        api_key=api_key
    )


def basic_chat_example(client: OpenAI):
    """Basic chat completion example."""
    print("=== Basic Chat Completion ===")
    
    response = client.chat.completions.create(
        model="claude-3-5-sonnet-20241022",
        messages=[
            {"role": "user", "content": "What is the capital of France?"}
        ]
    )
    
    print(f"Response: {response.choices[0].message.content}")
    print(f"Model: {response.model}")
    print(f"Usage: {response.usage}")
    print()


def system_message_example(client: OpenAI):
    """Chat with system message example."""
    print("=== Chat with System Message ===")
    
    response = client.chat.completions.create(
        model="claude-3-5-sonnet-20241022",
        messages=[
            {"role": "system", "content": "You are a helpful coding assistant. Be concise."},
            {"role": "user", "content": "How do I read a file in Python?"}
        ]
    )
    
    print(f"Response: {response.choices[0].message.content}")
    print()


def conversation_example(client: OpenAI):
    """Multi-turn conversation example."""
    print("=== Multi-turn Conversation ===")
    
    messages = [
        {"role": "user", "content": "My name is Alice."},
        {"role": "assistant", "content": "Nice to meet you, Alice! How can I help you today?"},
        {"role": "user", "content": "What's my name?"}
    ]
    
    response = client.chat.completions.create(
        model="claude-3-5-sonnet-20241022",
        messages=messages
    )
    
    print(f"Response: {response.choices[0].message.content}")
    print()


def streaming_example(client: OpenAI):
    """Streaming response example."""
    print("=== Streaming Response ===")
    
    stream = client.chat.completions.create(
        model="claude-3-5-sonnet-20241022",
        messages=[
            {"role": "user", "content": "Write a haiku about programming"}
        ],
        stream=True
    )
    
    print("Response: ", end="", flush=True)
    for chunk in stream:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
    print("\n")


def file_operation_example(client: OpenAI):
    """Example using Claude Code's file capabilities."""
    print("=== File Operation Example ===")
    
    response = client.chat.completions.create(
        model="claude-3-5-sonnet-20241022",
        messages=[
            {"role": "user", "content": "List the files in the current directory"}
        ]
    )
    
    print(f"Response: {response.choices[0].message.content}")
    print()


def code_generation_example(client: OpenAI):
    """Code generation example."""
    print("=== Code Generation Example ===")
    
    response = client.chat.completions.create(
        model="claude-3-5-sonnet-20241022",
        messages=[
            {"role": "user", "content": "Write a Python function that calculates fibonacci numbers"}
        ],
        temperature=0.7
    )
    
    print(f"Response:\n{response.choices[0].message.content}")
    print()


def list_models_example(client: OpenAI):
    """List available models."""
    print("=== Available Models ===")
    
    models = client.models.list()
    for model in models.data:
        print(f"- {model.id} (owned by: {model.owned_by})")
    print()


def error_handling_example(client: OpenAI):
    """Error handling example."""
    print("=== Error Handling Example ===")
    
    try:
        # This might fail if Claude Code has issues
        response = client.chat.completions.create(
            model="invalid-model",
            messages=[
                {"role": "user", "content": "Test"}
            ]
        )
    except Exception as e:
        print(f"Error occurred: {type(e).__name__}: {e}")
    print()


def main():
    """Run all examples."""
    # Create client
    client = create_client()
    
    # Run examples
    try:
        basic_chat_example(client)
        system_message_example(client)
        conversation_example(client)
        streaming_example(client)
        file_operation_example(client)
        code_generation_example(client)
        list_models_example(client)
        error_handling_example(client)
        
    except Exception as e:
        print(f"Failed to run examples: {e}")
        print("Make sure the Claude Code wrapper server is running on port 8000")


if __name__ == "__main__":
    main()