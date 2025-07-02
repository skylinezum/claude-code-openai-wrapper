# Claude Code OpenAI API Wrapper

This project provides an OpenAI API-compatible wrapper for Claude Code, allowing users to interact with Claude Code using OpenAI client libraries.

## Project Overview

- FastAPI server providing OpenAI-compatible endpoints
- Direct integration with Claude Code CLI (not SDK)
- Supports both streaming and non-streaming responses
- Automatic tool usage based on prompts
- Stateless architecture (each request spawns new Claude process)
- Uses Poetry for dependency management

## Development Guidelines

- Follow existing code patterns and conventions
- Maintain OpenAI API compatibility where possible
- Simplify responses where Claude Code doesn't provide equivalent data
- Handle errors gracefully with proper error messages
- Test with both OpenAI SDK and curl examples
- Use Poetry for all dependency management and virtual environments

## Key Implementation Notes

- Use subprocess to spawn Claude CLI with `--output-format stream_json`
- Parse JSON chunks line-by-line from stdout
- Convert OpenAI message format to Claude Code prompts
- Handle streaming via Server-Sent Events (SSE)
- No explicit tool configuration (tools work automatically)

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
   ```bash
   poetry run python main.py
   ```

## Testing

- Test basic chat completions: `poetry run python test_basic.py`
- Test streaming responses
- Verify OpenAI SDK compatibility
- Check error handling scenarios
- Run all tests: `poetry run pytest`
- Format code: `poetry run black .`