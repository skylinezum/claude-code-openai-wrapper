#!/usr/bin/env python3
"""
Basic test to verify the Claude Code OpenAI wrapper works.
Run this after starting the server to ensure everything is set up correctly.
"""

import sys
import requests
from openai import OpenAI

def test_health_check():
    """Test the health endpoint."""
    print("Testing health check...")
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print("✓ Health check passed")
            return True
        else:
            print(f"✗ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Cannot connect to server: {e}")
        return False

def test_models_endpoint():
    """Test the models endpoint."""
    print("\nTesting models endpoint...")
    try:
        response = requests.get("http://localhost:8000/v1/models")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Models endpoint works. Found {len(data['data'])} models")
            return True
        else:
            print(f"✗ Models endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Models endpoint error: {e}")
        return False

def test_openai_sdk():
    """Test with OpenAI SDK."""
    print("\nTesting OpenAI SDK integration...")
    try:
        client = OpenAI(
            base_url="http://localhost:8000/v1",
            api_key="dummy"  # Use dummy key if no auth configured
        )
        
        # Simple test
        response = client.chat.completions.create(
            model="claude-3-5-sonnet-20241022",
            messages=[
                {"role": "user", "content": "Say 'Hello, World!' and nothing else."}
            ],
            max_tokens=50
        )
        
        content = response.choices[0].message.content
        print(f"✓ OpenAI SDK test passed")
        print(f"  Response: {content}")
        return True
        
    except Exception as e:
        print(f"✗ OpenAI SDK test failed: {e}")
        return False

def test_streaming():
    """Test streaming functionality."""
    print("\nTesting streaming...")
    try:
        client = OpenAI(
            base_url="http://localhost:8000/v1",
            api_key="dummy"
        )
        
        stream = client.chat.completions.create(
            model="claude-3-5-sonnet-20241022",
            messages=[
                {"role": "user", "content": "Count from 1 to 3."}
            ],
            stream=True
        )
        
        chunks_received = 0
        content = ""
        for chunk in stream:
            chunks_received += 1
            if chunk.choices[0].delta.content:
                content += chunk.choices[0].delta.content
        
        if chunks_received > 0:
            print(f"✓ Streaming test passed ({chunks_received} chunks)")
            print(f"  Response: {content[:50]}...")
            return True
        else:
            print("✗ No streaming chunks received")
            return False
            
    except Exception as e:
        print(f"✗ Streaming test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("Claude Code OpenAI Wrapper - Basic Tests")
    print("="*50)
    print("Make sure the server is running: python main.py")
    print("="*50)
    
    tests = [
        test_health_check,
        test_models_endpoint,
        test_openai_sdk,
        test_streaming
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "="*50)
    print(f"Tests completed: {passed}/{len(tests)} passed")
    
    if passed == len(tests):
        print("✓ All tests passed! The wrapper is working correctly.")
        return 0
    else:
        print("✗ Some tests failed. Check the server logs for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())