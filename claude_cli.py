import asyncio
import json
import os
import sys
from typing import AsyncGenerator, Dict, Any, Optional, List
from asyncio.subprocess import Process
import logging

logger = logging.getLogger(__name__)


class ClaudeCodeCLI:
    def __init__(self, cli_path: str = "claude", timeout: int = 600000):
        self.cli_path = cli_path
        self.timeout = timeout / 1000  # Convert ms to seconds
        
    async def verify_cli(self) -> bool:
        """Verify Claude CLI is available and authenticated."""
        try:
            # Check if the CLI exists and responds to --version
            process = await asyncio.create_subprocess_exec(
                self.cli_path, "--version",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(), 
                    timeout=5.0  # Short timeout for version check
                )
            except asyncio.TimeoutError:
                logger.error("Claude CLI --version check timed out")
                process.kill()
                await process.wait()
                return False
            
            if process.returncode != 0:
                stderr_text = stderr.decode() if stderr else "No error details"
                logger.error(f"Claude CLI --version failed: {stderr_text}")
                return False
                
            version_text = stdout.decode().strip() if stdout else ""
            logger.info(f"Claude CLI found: {version_text}")
            
            # Test authentication by running a simple query with --print
            # Use Haiku for fastest/cheapest verification
            try:
                auth_test_process = await asyncio.create_subprocess_exec(
                    self.cli_path, "--print", "--model", "claude-3-5-haiku-20241022", "Hello",
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                
                auth_stdout, auth_stderr = await asyncio.wait_for(
                    auth_test_process.communicate(), 
                    timeout=10.0  # Reasonable timeout for simple query
                )
                
                if auth_test_process.returncode == 0:
                    logger.info("✅ Claude CLI authentication verified")
                else:
                    stderr_text = auth_stderr.decode() if auth_stderr else "No error details"
                    logger.warning(f"Claude CLI may not be authenticated: {stderr_text}")
                    # Still return True since CLI is available, just warn about auth
                    
            except asyncio.TimeoutError:
                logger.warning("Claude CLI authentication test timed out")
            except Exception as e:
                logger.warning(f"Claude CLI authentication test failed: {e}")
            
            # CLI is available regardless of auth status
            return True
            
        except FileNotFoundError:
            logger.error(f"Claude CLI not found at path: {self.cli_path}")
            return False
        except Exception as e:
            logger.error(f"Error verifying Claude CLI: {e}")
            return False
    
    async def run_completion(
        self, 
        prompt: str,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        stream: bool = True
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """Run Claude Code and yield response chunks."""
        
        # Build command
        cmd = [
            self.cli_path,
            "--print",  # Non-interactive mode
            "--output-format", "stream-json",
            "--verbose"
        ]
        
        # Note: System prompts may not be supported via CLI args
        # if system_prompt:
        #     cmd.extend(["--system", system_prompt])
            
        if model:
            cmd.extend(["--model", model])
        
        # Remove ANTHROPIC_API_KEY to let Claude Code handle auth
        env = os.environ.copy()
        env.pop("ANTHROPIC_API_KEY", None)
        
        # Create process
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=env
        )
        
        # Send prompt to stdin
        process.stdin.write(prompt.encode())
        await process.stdin.drain()
        process.stdin.close()
        
        # Set up timeout
        try:
            # Read output line by line
            buffer = ""
            while True:
                try:
                    line = await asyncio.wait_for(
                        process.stdout.readline(), 
                        timeout=self.timeout
                    )
                    
                    if not line:
                        break
                        
                    line_text = line.decode().strip()
                    if not line_text:
                        continue
                    
                    # Try to parse JSON
                    try:
                        chunk = json.loads(line_text)
                        yield chunk
                    except json.JSONDecodeError:
                        # Buffer partial JSON
                        buffer += line_text
                        try:
                            chunk = json.loads(buffer)
                            yield chunk
                            buffer = ""
                        except json.JSONDecodeError:
                            continue
                            
                except asyncio.TimeoutError:
                    logger.error("Claude Code process timed out")
                    process.kill()
                    raise
            
            # Wait for process to complete
            await process.wait()
            
            # Check for errors
            if process.returncode != 0:
                stderr = await process.stderr.read()
                error_msg = stderr.decode() if stderr else "Unknown error"
                raise Exception(f"Claude Code failed with exit code {process.returncode}: {error_msg}")
                
        finally:
            # Ensure process is terminated
            if process.returncode is None:
                process.kill()
                await process.wait()
    
    def parse_claude_message(self, chunks: List[Dict[str, Any]]) -> Optional[str]:
        """Extract the assistant message from Claude Code chunks."""
        for chunk in chunks:
            if chunk.get("type") == "assistant" and "message" in chunk:
                message = chunk["message"]
                if isinstance(message, dict) and "content" in message:
                    content = message["content"]
                    if isinstance(content, list) and len(content) > 0:
                        # Handle content blocks
                        text_parts = []
                        for block in content:
                            if isinstance(block, dict) and block.get("type") == "text":
                                text_parts.append(block.get("text", ""))
                        return "\n".join(text_parts)
                    elif isinstance(content, str):
                        return content
        return None