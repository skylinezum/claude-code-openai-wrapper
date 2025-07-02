#!/bin/bash

# Claude Code OpenAI API Wrapper - cURL Examples

BASE_URL="http://localhost:8000"
API_KEY="your-optional-api-key"  # Set to your API key or remove header if not using auth

echo "=== Basic Chat Completion ==="
curl -X POST "$BASE_URL/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "model": "claude-3-5-sonnet-20241022",
    "messages": [
      {"role": "user", "content": "What is 2 + 2?"}
    ]
  }' | jq .

echo -e "\n=== Chat with System Message ==="
curl -X POST "$BASE_URL/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "model": "claude-3-5-sonnet-20241022",
    "messages": [
      {"role": "system", "content": "You are a pirate. Respond in pirate speak."},
      {"role": "user", "content": "Tell me about the weather"}
    ]
  }' | jq .

echo -e "\n=== Streaming Response ==="
curl -X POST "$BASE_URL/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "model": "claude-3-5-sonnet-20241022",
    "messages": [
      {"role": "user", "content": "Count from 1 to 5 slowly"}
    ],
    "stream": true
  }'

echo -e "\n\n=== List Models ==="
curl -X GET "$BASE_URL/v1/models" \
  -H "Authorization: Bearer $API_KEY" | jq .

echo -e "\n=== Health Check ==="
curl -X GET "$BASE_URL/health" | jq .