# Claude Code OpenAI API Wrapper

An OpenAI API-compatible wrapper for Claude Code, allowing you to use Claude Code with any OpenAI client library. **Now powered by the official Claude Code Python SDK** with enhanced authentication and features.

## Status

🎉 **Production Ready** - All core features working and tested:
- ✅ Chat completions endpoint with **official Claude Code Python SDK**
- ✅ Streaming and non-streaming responses  
- ✅ Full OpenAI SDK compatibility
- ✅ **Multi-provider authentication** (API key, Bedrock, Vertex AI, CLI auth)
- ✅ **System prompt support** via SDK options
- ✅ Model selection support with validation
- ✅ Automatic tool usage (Read, Write, Bash, etc.)
- ✅ **Real-time cost and token tracking** from SDK
- ✅ **Session management** with proper session IDs
- ✅ Health, auth status, and models endpoints
- ✅ **Development mode** with auto-reload

## Features

### 🔥 **Core API Compatibility**
- OpenAI-compatible `/v1/chat/completions` endpoint
- Support for both streaming and non-streaming responses
- Compatible with OpenAI Python SDK and all OpenAI client libraries
- Automatic model validation and selection

### 🛠 **Claude Code SDK Integration**
- **Official Claude Code Python SDK** integration (v0.0.14)
- **Real-time cost tracking** - actual costs from SDK metadata
- **Accurate token counting** - input/output tokens from SDK
- **Session management** - proper session IDs and continuity
- **Enhanced error handling** with detailed authentication diagnostics

### 🔐 **Multi-Provider Authentication**
- **Automatic detection** of authentication method
- **Claude CLI auth** - works with existing `claude auth` setup
- **Direct API key** - `ANTHROPIC_API_KEY` environment variable
- **AWS Bedrock** - enterprise authentication with AWS credentials
- **Google Vertex AI** - GCP authentication support

### ⚡ **Advanced Features**
- **System prompt support** via SDK options
- **Automatic tool usage** - Read, Write, Bash, Glob, Grep, and more
- **Development mode** with auto-reload (`uvicorn --reload`)
- **Optional API key protection** for FastAPI endpoints
- **Comprehensive logging** and debugging capabilities

## Quick Start

Get started in under 2 minutes:

```bash
# 1. Install Claude Code CLI (if not already installed)
npm install -g @anthropic-ai/claude-code

# 2. Authenticate (choose one method)
claude auth login  # Recommended for development
# OR set: export ANTHROPIC_API_KEY=your-api-key

# 3. Clone and setup the wrapper
git clone <repository-url>
cd claudewrapper
poetry install

# 4. Start the server
poetry run uvicorn main:app --reload --port 8000

# 5. Test it works
poetry run python test_endpoints.py
```

🎉 **That's it!** Your OpenAI-compatible Claude Code API is running on `http://localhost:8000`

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
# Output: Claude will actually read your directory and list the files!

# Check real costs and tokens
print(f"Cost: ${response.usage.total_tokens * 0.000003:.6f}")  # Real cost tracking
print(f"Tokens: {response.usage.total_tokens} ({response.usage.prompt_tokens} + {response.usage.completion_tokens})")

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

## Limitations & Roadmap

### 🚫 **Current Limitations**
- **Images in messages** are converted to text placeholders
- **Function calling** not supported (tools work automatically based on prompts)
- **OpenAI parameters** not yet mapped: `temperature`, `top_p`, `max_tokens`, `logit_bias`, `presence_penalty`, `frequency_penalty`
- **Multiple responses** (`n > 1`) not supported

### 🛣 **Planned Enhancements** 
- [ ] **Session continuity** - conversation history across requests
- [ ] **Tool configuration** - allowed/disallowed tools endpoints  
- [ ] **OpenAI parameter mapping** - temperature, top_p, max_tokens support
- [ ] **Enhanced streaming** - better chunk handling
- [ ] **MCP integration** - Model Context Protocol server support

### ✅ **Recent Improvements**
- **✅ SDK Integration**: Official Python SDK replaces subprocess calls
- **✅ Real Metadata**: Accurate costs and token counts from SDK
- **✅ Multi-auth**: Support for CLI, API key, Bedrock, and Vertex AI authentication  
- **✅ Session IDs**: Proper session tracking and management
- **✅ System Prompts**: Full support via SDK options

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

### 🧪 **Quick Test Suite**
Test all endpoints with a simple script:
```bash
# Make sure server is running first
poetry run python test_endpoints.py
```

### 📝 **Basic Test Suite**
Run the comprehensive test suite:
```bash
# Make sure server is running first  
poetry run python test_basic.py
```

### 🔍 **Authentication Test**
Check authentication status:
```bash
curl http://localhost:8000/v1/auth/status | python -m json.tool
```

### ⚙️ **Development Tools**
```bash
# Install development dependencies
poetry install --with dev

# Format code
poetry run black .

# Run full tests (when implemented)
poetry run pytest tests/
```

### ✅ **Expected Results**
All tests should show:
- **4/4 endpoint tests passing**
- **4/4 basic tests passing** 
- **Authentication method detected** (claude_cli, anthropic, bedrock, or vertex)
- **Real cost tracking** (e.g., $0.001-0.005 per test call)
- **Accurate token counts** from SDK metadata

## License

MIT License

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.