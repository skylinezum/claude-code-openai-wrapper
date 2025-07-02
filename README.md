# Claude Code OpenAI API Wrapper

An OpenAI API-compatible wrapper for Claude Code, allowing you to use Claude Code with any OpenAI client library.

## Features

- OpenAI-compatible `/v1/chat/completions` endpoint
- Support for both streaming and non-streaming responses
- Automatic tool usage based on prompts (Read, Write, Bash, etc.)
- Optional API key authentication
- Compatible with OpenAI Python SDK and other OpenAI clients

## Prerequisites

1. **Claude Code CLI**: Install and authenticate Claude Code CLI
   ```bash
   # Install Claude Code (follow Anthropic's official guide)
   # Then authenticate:
   claude auth login
   ```

2. **Python 3.10+**: Required for the server

3. **Poetry**: For dependency management
   ```bash
   # Install Poetry (if not already installed)
   curl -sSL https://install.python-poetry.org | python3 -
   ```

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd claudewrapper
   ```

2. Install dependencies with Poetry:
   ```bash
   poetry install
   ```

   This will create a virtual environment and install all dependencies.

3. Configure environment:
   ```bash
   cp .env.example .env
   # Edit .env with your preferences
   ```

## Configuration

Edit the `.env` file:

```env
# Claude CLI path (usually just "claude")
CLAUDE_CLI_PATH=claude

# Optional API key for client authentication
# Leave empty to allow unauthenticated access
API_KEY=your-optional-api-key

# Server port
PORT=8000

# Timeout in milliseconds
MAX_TIMEOUT=600000

# CORS origins
CORS_ORIGINS=["*"]
```

## Running the Server

1. Ensure Claude Code is authenticated:
   ```bash
   claude auth status
   ```

2. Start the server:
   ```bash
   poetry run python main.py
   ```

   Or with uvicorn:
   ```bash
   poetry run uvicorn main:app --reload --port 8000
   ```

## Usage Examples

### Using curl

```bash
# Basic chat completion
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-optional-api-key" \
  -d '{
    "model": "claude-3-5-sonnet-20241022",
    "messages": [
      {"role": "user", "content": "What is 2 + 2?"}
    ]
  }'

# Streaming response
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-optional-api-key" \
  -d '{
    "model": "claude-3-5-sonnet-20241022",
    "messages": [
      {"role": "user", "content": "Write a Python hello world script"}
    ],
    "stream": true
  }'
```

### Using OpenAI Python SDK

```python
from openai import OpenAI

# Configure client to use local server
client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="your-optional-api-key"  # or "dummy" if no auth
)

# Basic chat completion
response = client.chat.completions.create(
    model="claude-3-5-sonnet-20241022",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What files are in the current directory?"}
    ]
)

print(response.choices[0].message.content)

# Streaming
stream = client.chat.completions.create(
    model="claude-3-5-sonnet-20241022",
    messages=[
        {"role": "user", "content": "Explain quantum computing"}
    ],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

## Supported Models

- `claude-sonnet-4-20250514` (Recommended)
- `claude-opus-4-20250514`
- `claude-3-7-sonnet-20250219`
- `claude-3-5-sonnet-20241022`
- `claude-3-5-haiku-20241022`

Note: Model parameter is currently ignored, and Claude Code will use its default model.

## API Endpoints

- `POST /v1/chat/completions` - OpenAI-compatible chat completions
- `GET /v1/models` - List available models
- `GET /health` - Health check endpoint

## Limitations

- Images in messages are converted to text placeholders
- Token usage is estimated (not exact)
- Each request spawns a new Claude process (stateless)
- No support for function calling (tools work automatically)
- No support for logit_bias, presence_penalty, frequency_penalty

## Troubleshooting

1. **Claude CLI not found**:
   ```bash
   # Check Claude is in PATH
   which claude
   # Update CLAUDE_CLI_PATH in .env if needed
   ```

2. **Authentication errors**:
   ```bash
   # Re-authenticate Claude Code
   claude auth logout
   claude auth login
   ```

3. **Timeout errors**:
   - Increase `MAX_TIMEOUT` in `.env`
   - Note: Claude Code can take time for complex requests

## Development

Run tests:
```bash
poetry run pytest tests/
```

Format code:
```bash
poetry run black .
```

Install development dependencies:
```bash
poetry install --with dev
```

## License

MIT License

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.