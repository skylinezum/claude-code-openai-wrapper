# Claude Code OpenAI API Wrapper

An OpenAI API-compatible wrapper for Claude Code, allowing you to use Claude Code with any OpenAI client library. **Now powered by the official Claude Code Python SDK** with enhanced authentication and features.

## Status

✅ **Fully functional** - All core features working and tested:
- ✅ Chat completions endpoint with **SDK integration**
- ✅ Streaming responses  
- ✅ OpenAI SDK compatibility
- ✅ **Enhanced authentication** (API key, Bedrock, Vertex AI, CLI auth)
- ✅ **System prompt support** 
- ✅ Model selection support
- ✅ Automatic tool usage
- ✅ **Real cost and metadata tracking**
- ✅ Health and models endpoints

## Features

- OpenAI-compatible `/v1/chat/completions` endpoint
- **NEW**: Official Claude Code Python SDK integration (v0.0.14)
- **NEW**: Multiple authentication methods with automatic detection
- **NEW**: System prompt support via SDK options
- **NEW**: Enhanced metadata extraction (costs, tokens, session IDs)
- Support for both streaming and non-streaming responses
- Automatic tool usage based on prompts (Read, Write, Bash, etc.)
- Optional API key authentication
- Compatible with OpenAI Python SDK and other OpenAI clients

## Prerequisites

1. **Claude Code CLI**: Install Claude Code CLI
   ```bash
   # Install Claude Code (follow Anthropic's official guide)
   npm install -g @anthropic-ai/claude-code
   ```

2. **Authentication**: Choose one method:
   - **Option A**: Authenticate via CLI (Recommended for development)
     ```bash
     claude auth login
     ```
   - **Option B**: Set environment variable
     ```bash
     export ANTHROPIC_API_KEY=your-api-key
     ```
   - **Option C**: Use AWS Bedrock or Google Vertex AI (see Configuration section)

3. **Python 3.10+**: Required for the server

4. **Poetry**: For dependency management
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
# Comment out or leave empty to allow unauthenticated access
# API_KEY=your-optional-api-key

# Server port
PORT=8000

# Timeout in milliseconds
MAX_TIMEOUT=600000

# CORS origins
CORS_ORIGINS=["*"]
```

## Running the Server

1. Verify Claude Code is installed and working:
   ```bash
   claude --version
   claude --print --model claude-3-5-haiku-20241022 "Hello"  # Test with fastest model
   ```

2. Start the server:

   **Development mode (recommended - auto-reloads on changes):**
   ```bash
   poetry run uvicorn main:app --reload --port 8000
   ```

   **Production mode:**
   ```bash
   poetry run python main.py
   ```

   **Port Options for production mode:**
   - Default: Uses port 8000 (or PORT from .env)
   - If port is in use, automatically finds next available port
   - Specify custom port: `poetry run python main.py 9000`
   - Set in environment: `PORT=9000 poetry run python main.py`

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

The model parameter is passed to Claude Code via the `--model` flag.

## API Endpoints

- `POST /v1/chat/completions` - OpenAI-compatible chat completions
- `GET /v1/models` - List available models
- `GET /v1/auth/status` - **NEW**: Check authentication status and configuration
- `GET /health` - Health check endpoint

## Limitations

- Images in messages are converted to text placeholders
- **IMPROVED**: Token usage and costs now more accurate via SDK metadata
- **IMPROVED**: Better session management via SDK (was stateless CLI spawning)
- No support for function calling (tools work automatically)
- No support for logit_bias, presence_penalty, frequency_penalty
- Some OpenAI parameters (temperature, top_p) not yet mapped to SDK options

## Troubleshooting

1. **Claude CLI not found**:
   ```bash
   # Check Claude is in PATH
   which claude
   # Update CLAUDE_CLI_PATH in .env if needed
   ```

2. **Authentication errors**:
   ```bash
   # Test authentication with fastest model
   claude --print --model claude-3-5-haiku-20241022 "Hello"
   # If this fails, re-authenticate if needed
   ```

3. **Timeout errors**:
   - Increase `MAX_TIMEOUT` in `.env`
   - Note: Claude Code can take time for complex requests

## Testing

Run the basic test suite:
```bash
# Make sure server is running first
poetry run python test_basic.py
```

Run full tests:
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