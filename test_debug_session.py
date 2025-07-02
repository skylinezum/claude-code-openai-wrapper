#!/usr/bin/env python3
"""
Debug test for session continuity.
"""

import requests
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

BASE_URL = "http://localhost:8000"
SESSION_ID = "debug-session"

def test_debug():
    print("🧪 Testing session with debug logging...")
    
    # First request
    print("\n1️⃣ First request (introducing name)...")
    response1 = requests.post(f"{BASE_URL}/v1/chat/completions", json={
        "model": "claude-3-5-sonnet-20241022",
        "messages": [
            {"role": "user", "content": "Hello! My name is Bob."}
        ],
        "session_id": SESSION_ID
    })
    
    if response1.status_code == 200:
        result1 = response1.json()
        print(f"Response 1: {result1['choices'][0]['message']['content'][:100]}...")
    else:
        print(f"Request 1 failed: {response1.status_code}")
        return
    
    # Second request
    print("\n2️⃣ Second request (asking about name)...")
    response2 = requests.post(f"{BASE_URL}/v1/chat/completions", json={
        "model": "claude-3-5-sonnet-20241022", 
        "messages": [
            {"role": "user", "content": "What's my name?"}
        ],
        "session_id": SESSION_ID
    })
    
    if response2.status_code == 200:
        result2 = response2.json()
        print(f"Response 2: {result2['choices'][0]['message']['content'][:100]}...")
        
        if "bob" in result2['choices'][0]['message']['content'].lower():
            print("✅ Session continuity working!")
        else:
            print("❌ Session continuity not working")
    else:
        print(f"Request 2 failed: {response2.status_code}")
    
    # Clean up
    requests.delete(f"{BASE_URL}/v1/sessions/{SESSION_ID}")

if __name__ == "__main__":
    test_debug()