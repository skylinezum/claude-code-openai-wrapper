# OpenAI to Claude Code SDK Parameter Mapping

This document provides a comprehensive mapping between OpenAI Chat Completions API parameters and Claude Code SDK options, including handling of unsupported parameters and validation logic.

## Quick Reference

### ✅ Fully Supported Parameters

| OpenAI Parameter | Claude SDK Option | Notes |
|------------------|-------------------|-------|
| `model` | `options.model` | Direct mapping to Claude models |
| `messages` (system) | `options.system_prompt` | System messages extracted automatically |
| `stream` | Built-in | SDK natively supports streaming via AsyncIterator |
| `user` | Logging/Analytics | Used for request tracking and session identification |

### 🚫 Unsupported Parameters (Logged & Ignored)

| OpenAI Parameter | Claude SDK | Reason | Alternative |
|------------------|------------|---------|-------------|
| `temperature` | ❌ Not available | Claude Code SDK doesn't expose sampling parameters | Use different models for varied response styles |
| `top_p` | ❌ Not available | Claude Code SDK doesn't expose sampling parameters | Not available |
| `max_tokens` | ❌ Not available | Different response length control model | Use `max_turns` or `max_thinking_tokens` |
| `presence_penalty` | ❌ Not available | Claude Code SDK doesn't support penalty parameters | Use system prompt guidance |
| `frequency_penalty` | ❌ Not available | Claude Code SDK doesn't support penalty parameters | Use system prompt guidance |
| `logit_bias` | ❌ Not available | Claude Code SDK doesn't expose token-level control | Use system prompt guidance |
| `stop` | ❌ Not available | No stop sequence support | Post-process responses |
| `n` > 1 | ❌ Not supported | Only single response generation supported | Make multiple API calls |

### 🔧 Claude Code SDK Specific Options

| SDK Option | Default | Purpose | How to Use |
|------------|---------|---------|------------|
| `max_turns` | `10` | Limit conversation length | Custom header: `X-Claude-Max-Turns: 5` |
| `allowed_tools` | `[]` | Restrict available tools | Custom header: `X-Claude-Allowed-Tools: ls,cat,grep` |
| `disallowed_tools` | `[]` | Block specific tools | Custom header: `X-Claude-Disallowed-Tools: rm,mv` |
| `permission_mode` | `None` | Control tool permissions | Custom header: `X-Claude-Permission-Mode: acceptEdits` |
| `max_thinking_tokens` | `8000` | Limit internal reasoning | Custom header: `X-Claude-Max-Thinking-Tokens: 5000` |

## Implementation Details

### Parameter Validation

The wrapper implements comprehensive parameter validation:

```python
# Validation in models.py
@validator('n')
def validate_n(cls, v):
    if v > 1:
        raise ValueError("Claude Code SDK does not support multiple choices (n > 1)")
    return v

# Usage logging and warnings
def log_unsupported_parameters(self):
    warnings = []
    if self.temperature != 1.0:
        warnings.append(f"temperature={self.temperature} will be ignored")
    # ... additional parameter checks
```

### Custom Headers for Claude-Specific Options

You can pass Claude Code SDK specific parameters via HTTP headers:

```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "X-Claude-Max-Turns: 5" \
  -H "X-Claude-Allowed-Tools: ls,cat,grep" \
  -H "X-Claude-Permission-Mode: acceptEdits" \
  -d '{
    "model": "claude-3-5-sonnet-20241022",
    "messages": [{"role": "user", "content": "List files in current directory"}]
  }'
```

### Model Validation

The wrapper validates that requested models are supported by Claude Code SDK:

```python
SUPPORTED_MODELS = {
    "claude-sonnet-4-20250514",
    "claude-opus-4-20250514", 
    "claude-3-7-sonnet-20250219",
    "claude-3-5-sonnet-20241022",
    "claude-3-5-haiku-20241022"
}
```

## Usage Examples

### Basic OpenAI-Compatible Request

```python
import openai

client = openai.OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="dummy"  # Required by OpenAI client, not used by wrapper
)

response = client.chat.completions.create(
    model="claude-3-5-sonnet-20241022",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ],
    temperature=0.7,  # Will be logged as unsupported and ignored
    max_tokens=100    # Will be logged as unsupported and ignored
)
```

### Using Claude-Specific Features

```python
import requests

response = requests.post("http://localhost:8000/v1/chat/completions", 
    headers={
        "X-Claude-Max-Turns": "3",
        "X-Claude-Allowed-Tools": "ls,cat,pwd",
        "X-Claude-Permission-Mode": "acceptEdits"
    },
    json={
        "model": "claude-3-5-sonnet-20241022",
        "messages": [
            {"role": "user", "content": "Help me explore this directory"}
        ]
    }
)
```

### Checking Compatibility

Use the `/v1/compatibility` endpoint to check which parameters are supported:

```python
import requests

compatibility = requests.post("http://localhost:8000/v1/compatibility", json={
    "model": "claude-3-5-sonnet-20241022",
    "messages": [{"role": "user", "content": "test"}],
    "temperature": 0.8,
    "max_tokens": 100,
    "presence_penalty": 0.1
})

print(compatibility.json())
```

## Error Handling

### Validation Errors

Parameters that violate constraints will return HTTP 422:

```json
{
  "detail": [
    {
      "loc": ["body", "n"],
      "msg": "Claude Code SDK does not support multiple choices (n > 1). Only single response generation is supported.",
      "type": "value_error"
    }
  ]
}
```

### Unsupported Parameter Warnings

Unsupported parameters are logged as warnings but don't cause request failure:

```
WARNING:models:OpenAI API compatibility: temperature=0.7 is not supported by Claude Code SDK and will be ignored
WARNING:models:OpenAI API compatibility: max_tokens=100 is not supported by Claude Code SDK and will be ignored. Consider using max_turns to limit conversation length
```

## Migration Guide

### From OpenAI API to Claude Code Wrapper

1. **Change base URL**: Point your OpenAI client to the wrapper endpoint
2. **Update models**: Use Claude model names instead of GPT models
3. **Remove unsupported parameters**: Or accept that they'll be ignored
4. **Add Claude-specific headers**: For advanced features like tool restrictions

### Example Migration

Before (OpenAI):
```python
response = openai.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello"}],
    temperature=0.7,
    max_tokens=100
)
```

After (Claude Code Wrapper):
```python
response = openai.chat.completions.create(
    model="claude-3-5-sonnet-20241022",  # Changed model
    messages=[{"role": "user", "content": "Hello"}],
    # temperature and max_tokens will be ignored with warnings
)
```

## Testing

Run the parameter mapping tests:

```bash
# Start the server
poetry run python main.py

# In another terminal, run tests
poetry run python test_parameter_mapping.py
```

## Logging

Enable detailed logging to see parameter warnings:

```bash
# Set logging level to see all warnings
PYTHONPATH=. poetry run python -c "
import logging
logging.basicConfig(level=logging.DEBUG)
exec(open('main.py').read())
"
```

## Code Structure

The parameter mapping implementation consists of:

- `models.py`: Request validation and parameter mapping
- `parameter_validator.py`: Validation logic and compatibility reporting
- `claude_cli.py`: SDK interface with parameter passing
- `main.py`: HTTP request handling and header extraction

## Compatibility Report

The wrapper provides a detailed compatibility report showing:
- Supported parameters in your request
- Unsupported parameters with explanations
- Suggestions for alternatives
- Available Claude Code SDK options

This comprehensive mapping ensures maximum compatibility while providing clear guidance on limitations and alternatives.