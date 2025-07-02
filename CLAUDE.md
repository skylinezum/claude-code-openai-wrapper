# Claude Code OpenAI API Wrapper

This project provides an OpenAI API-compatible wrapper for Claude Code, allowing users to interact with Claude Code using OpenAI client libraries.

## Project Overview

- FastAPI server providing OpenAI-compatible endpoints
- **NEW**: Direct integration with Claude Code Python SDK (v0.0.14)
- Supports both streaming and non-streaming responses
- Automatic tool usage based on prompts
- **NEW**: Enhanced authentication with multiple provider support
- **NEW**: System prompt support via SDK options
- **NEW**: Improved metadata extraction (costs, tokens, session IDs)
- Uses Poetry for dependency management

## Development Guidelines

- Follow existing code patterns and conventions
- Maintain OpenAI API compatibility where possible
- Simplify responses where Claude Code doesn't provide equivalent data
- Handle errors gracefully with proper error messages
- Test with both OpenAI SDK and curl examples
- Use Poetry for all dependency management and virtual environments

## Key Implementation Notes

- **NEW**: Uses official Claude Code Python SDK (`claude-code-sdk`)
- **NEW**: Multiple authentication methods supported (API key, Bedrock, Vertex AI, CLI auth)
- Convert OpenAI message format to Claude Code prompts
- Handle streaming via Server-Sent Events (SSE)
- **NEW**: Enhanced error handling and authentication validation
- **NEW**: Real cost and metadata extraction from SDK responses

## Development Setup

1. Install Poetry if not already installed:
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. Install dependencies:
   ```bash
   poetry install --with dev
   ```

3. Run the server:
   
   **Development mode (auto-reload on file changes):**
   ```bash
   poetry run uvicorn main:app --reload --port 8000
   ```
   
   **Production mode:**
   ```bash
   poetry run python main.py
   ```

## Authentication

The wrapper now supports multiple Claude Code authentication methods:

### Method 1: Claude CLI Authentication (Recommended for Development)
If you're already authenticated with Claude Code CLI, no additional setup is needed:
```bash
claude auth  # If not already authenticated
poetry run python main.py
```

### Method 2: Direct Anthropic API Key
```bash
export ANTHROPIC_API_KEY=your-api-key
poetry run python main.py
```

### Method 3: AWS Bedrock (Enterprise)
```bash
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_ACCESS_KEY_ID=your-access-key
export AWS_SECRET_ACCESS_KEY=your-secret-key
export AWS_REGION=us-east-1
poetry run python main.py
```

### Method 4: Google Vertex AI (GCP)
```bash
export CLAUDE_CODE_USE_VERTEX=1
export ANTHROPIC_VERTEX_PROJECT_ID=your-project-id
export CLOUD_ML_REGION=us-east5
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
poetry run python main.py
```

## API Endpoints

- `GET /health` - Health check endpoint
- `GET /v1/auth/status` - Check authentication status and configuration
- `GET /v1/models` - List available Claude models
- `POST /v1/chat/completions` - OpenAI-compatible chat completions

## Testing

- Test basic chat completions: `poetry run python test_basic.py`
- Test streaming responses
- Verify OpenAI SDK compatibility
- Check error handling scenarios
- Run all tests: `poetry run pytest`
- Format code: `poetry run black .`

## New Features in SDK Integration

- **Enhanced Authentication**: Multiple provider support with automatic detection
- **System Prompts**: Full support via SDK `system_prompt` option
- **Real Metadata**: Accurate cost tracking, token counts, and session IDs from SDK
- **Better Error Handling**: Comprehensive authentication validation and error reporting
- **Improved Streaming**: Enhanced streaming response handling with proper message conversion

## Git Workflow

- Please create a new branch before making any changes