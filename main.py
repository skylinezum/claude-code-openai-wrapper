import os
import json
import asyncio
import logging
from typing import Optional, AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from dotenv import load_dotenv

from models import (
    ChatCompletionRequest, 
    ChatCompletionResponse, 
    ChatCompletionStreamResponse,
    Choice, 
    Message, 
    Usage,
    StreamChoice,
    ErrorResponse,
    ErrorDetail
)
from claude_cli import ClaudeCodeCLI
from message_adapter import MessageAdapter
from auth import verify_api_key

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Claude CLI
claude_cli = ClaudeCodeCLI(
    cli_path=os.getenv("CLAUDE_CLI_PATH", "claude"),
    timeout=int(os.getenv("MAX_TIMEOUT", "600000"))
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Verify Claude CLI on startup."""
    logger.info("Verifying Claude Code CLI...")
    if not await claude_cli.verify_cli():
        logger.error("Failed to verify Claude Code CLI. Please ensure it's installed and authenticated.")
        raise RuntimeError("Claude Code CLI verification failed")
    logger.info("Claude Code CLI verified successfully")
    yield


# Create FastAPI app
app = FastAPI(
    title="Claude Code OpenAI API Wrapper",
    description="OpenAI-compatible API for Claude Code",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
cors_origins = json.loads(os.getenv("CORS_ORIGINS", '["*"]'))
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def generate_streaming_response(
    request: ChatCompletionRequest,
    request_id: str
) -> AsyncGenerator[str, None]:
    """Generate SSE formatted streaming response."""
    try:
        # Convert messages to prompt
        prompt, system_prompt = MessageAdapter.messages_to_prompt(request.messages)
        
        # Filter content for unsupported features
        prompt = MessageAdapter.filter_content(prompt)
        if system_prompt:
            system_prompt = MessageAdapter.filter_content(system_prompt)
        
        # Run Claude Code
        chunks_buffer = []
        async for chunk in claude_cli.run_completion(
            prompt=prompt,
            system_prompt=system_prompt,
            model=request.model if request.model else None,
            stream=True
        ):
            chunks_buffer.append(chunk)
            
            # Check if we have an assistant message
            if chunk.get("type") == "assistant" and "message" in chunk:
                message = chunk["message"]
                if isinstance(message, dict) and "content" in message:
                    content = message["content"]
                    
                    # Handle content blocks
                    if isinstance(content, list):
                        for block in content:
                            if isinstance(block, dict) and block.get("type") == "text":
                                text = block.get("text", "")
                                
                                # Create streaming chunk
                                stream_chunk = ChatCompletionStreamResponse(
                                    id=request_id,
                                    model=request.model,
                                    choices=[StreamChoice(
                                        index=0,
                                        delta={"content": text},
                                        finish_reason=None
                                    )]
                                )
                                
                                yield f"data: {stream_chunk.model_dump_json()}\n\n"
                    
                    elif isinstance(content, str):
                        # Create streaming chunk
                        stream_chunk = ChatCompletionStreamResponse(
                            id=request_id,
                            model=request.model,
                            choices=[StreamChoice(
                                index=0,
                                delta={"content": content},
                                finish_reason=None
                            )]
                        )
                        
                        yield f"data: {stream_chunk.model_dump_json()}\n\n"
        
        # Send final chunk with finish reason
        final_chunk = ChatCompletionStreamResponse(
            id=request_id,
            model=request.model,
            choices=[StreamChoice(
                index=0,
                delta={},
                finish_reason="stop"
            )]
        )
        yield f"data: {final_chunk.model_dump_json()}\n\n"
        yield "data: [DONE]\n\n"
        
    except Exception as e:
        logger.error(f"Streaming error: {e}")
        error_chunk = {
            "error": {
                "message": str(e),
                "type": "streaming_error"
            }
        }
        yield f"data: {json.dumps(error_chunk)}\n\n"


@app.post("/v1/chat/completions", dependencies=[Depends(verify_api_key)])
async def chat_completions(request: ChatCompletionRequest):
    """OpenAI-compatible chat completions endpoint."""
    try:
        request_id = f"chatcmpl-{os.urandom(8).hex()}"
        
        if request.stream:
            # Return streaming response
            return StreamingResponse(
                generate_streaming_response(request, request_id),
                media_type="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                }
            )
        else:
            # Non-streaming response
            # Convert messages to prompt
            prompt, system_prompt = MessageAdapter.messages_to_prompt(request.messages)
            
            # Filter content
            prompt = MessageAdapter.filter_content(prompt)
            if system_prompt:
                system_prompt = MessageAdapter.filter_content(system_prompt)
            
            # Collect all chunks
            chunks = []
            async for chunk in claude_cli.run_completion(
                prompt=prompt,
                system_prompt=system_prompt,
                model=request.model if request.model else None,
                stream=False
            ):
                chunks.append(chunk)
            
            # Extract assistant message
            assistant_content = claude_cli.parse_claude_message(chunks)
            
            if not assistant_content:
                raise HTTPException(status_code=500, detail="No response from Claude Code")
            
            # Estimate tokens (rough approximation)
            prompt_tokens = MessageAdapter.estimate_tokens(prompt)
            completion_tokens = MessageAdapter.estimate_tokens(assistant_content)
            
            # Create response
            response = ChatCompletionResponse(
                id=request_id,
                model=request.model,
                choices=[Choice(
                    index=0,
                    message=Message(role="assistant", content=assistant_content),
                    finish_reason="stop"
                )],
                usage=Usage(
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                    total_tokens=prompt_tokens + completion_tokens
                )
            )
            
            return response
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Chat completion error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/v1/models")
async def list_models():
    """List available models."""
    return {
        "object": "list",
        "data": [
            {"id": "claude-sonnet-4-20250514", "object": "model", "owned_by": "anthropic"},
            {"id": "claude-opus-4-20250514", "object": "model", "owned_by": "anthropic"},
            {"id": "claude-3-7-sonnet-20250219", "object": "model", "owned_by": "anthropic"},
            {"id": "claude-3-5-sonnet-20241022", "object": "model", "owned_by": "anthropic"},
            {"id": "claude-3-5-haiku-20241022", "object": "model", "owned_by": "anthropic"},
        ]
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "claude-code-openai-wrapper"}


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Format HTTP exceptions as OpenAI-style errors."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "message": exc.detail,
                "type": "api_error",
                "code": str(exc.status_code)
            }
        }
    )


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)