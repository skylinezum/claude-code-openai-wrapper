# Claude Code SDK Integration - Implementation Plan

## Overview
This plan outlines the migration from direct CLI subprocess calls to the official Claude Code Python SDK, adding enhanced features and improving OpenAI API compatibility.

## Current Status
- ✅ Created new branch: `sdk-integration`
- ✅ Installed `claude-code-sdk` dependency via Poetry
- ✅ Rewrote `claude_cli.py` to use Python SDK instead of subprocess

## Phase 1: Core SDK Migration (High Priority)

### 1. ✅ Install Claude Code SDK
- Added `claude-code-sdk` to Poetry dependencies
- Version: 0.0.14

### 2. ✅ Replace CLI Integration 
- Completely rewrote `claude_cli.py` to use Python SDK
- Added support for ClaudeCodeOptions configuration
- Implemented proper async message streaming
- Added metadata extraction capabilities

### 3. 🔄 Update Authentication Support
- **Current**: Basic API key validation
- **Target**: Support for third-party providers (Bedrock, Vertex AI)
- **Files to modify**: `auth.py`, `main.py`
- **Implementation**: 
  - Add environment variable detection for `CLAUDE_CODE_USE_BEDROCK`, `CLAUDE_CODE_USE_VERTEX`
  - Update SDK options to pass through authentication method
  - Add validation for required credentials

### 4. 🔄 Fix System Prompt Support
- **Current**: System prompts commented out
- **Target**: Full system prompt support via SDK
- **Files to modify**: `main.py`
- **Implementation**: 
  - Pass system_prompt to `run_completion()`
  - Use SDK's `system_prompt` option
  - Update message adapter if needed

## Phase 2: Enhanced Features (Medium Priority)

### 5. 🔄 Session Management & Continuity
- **Current**: Stateless (each request spawns new process)
- **Target**: Support for conversation continuity and session tracking
- **Files to modify**: `main.py`, `models.py`
- **Implementation**:
  - Add session tracking endpoints
  - Support `--continue` and `--resume` functionality
  - Add session ID to request/response models
  - Implement session storage mechanism

### 6. 🔄 Tool Configuration Support
- **Current**: Automatic tool usage only
- **Target**: Configurable tool restrictions
- **Files to modify**: `main.py`, `models.py`
- **Implementation**:
  - Add `allowed_tools` and `disallowed_tools` to request model
  - Pass tool restrictions to SDK options
  - Add validation for tool names

### 7. 🔄 Enhanced Response Parsing
- **Current**: Basic token estimation
- **Target**: Accurate metadata from SDK responses
- **Files to modify**: `main.py`
- **Implementation**:
  - Use `extract_metadata()` method for accurate costs and tokens
  - Update Usage model with real data from SDK
  - Add session_id to responses

### 8. 🔄 Improved Streaming
- **Current**: Basic SSE streaming
- **Target**: Enhanced streaming with proper chunk handling
- **Files to modify**: `main.py`
- **Implementation**:
  - Better handling of SDK message types
  - Proper streaming error handling
  - Support for tool usage in streaming responses

## Phase 3: OpenAI Compatibility Improvements (Low Priority)

### 9. 🔄 Model Parameter Support
- **Files to modify**: `main.py`, `models.py`
- **Implementation**:
  - Map OpenAI parameters (temperature, top_p, max_tokens) to SDK options
  - Add parameter validation
  - Update request models with proper constraints

### 10. 🔄 Enhanced Error Handling
- **Files to modify**: `main.py`
- **Implementation**:
  - Map SDK errors to OpenAI error format
  - Add proper error codes and types
  - Improve error messages for debugging

### 11. 🔄 Cost Tracking
- **Files to modify**: `main.py`, `models.py`
- **Implementation**:
  - Use real cost data from SDK responses
  - Add cost tracking to response metadata
  - Consider adding cost limits/warnings

### 12. 🔄 Permission Modes
- **Files to modify**: `main.py`, `models.py`
- **Implementation**:
  - Add support for permission modes (acceptEdits, bypassPermissions, plan)
  - Map to SDK options
  - Add configuration endpoints

## Phase 4: Advanced Features (Optional)

### 13. 🔄 MCP Integration
- **Files to modify**: New endpoints, `main.py`
- **Implementation**:
  - Add MCP server configuration endpoints
  - Support `--mcp-config` equivalent
  - Add MCP tool management

### 14. 🔄 Custom Tool APIs
- **Files to modify**: New endpoints
- **Implementation**:
  - Add endpoints for tool configuration
  - Tool status and capabilities
  - Custom tool definitions

### 15. 🔄 Session Management API
- **Files to modify**: New endpoints
- **Implementation**:
  - List sessions endpoint
  - Session history endpoint
  - Session deletion/management

## Testing Plan

### Unit Tests
- Test SDK integration with mock responses
- Test message parsing and adaptation
- Test error handling scenarios

### Integration Tests
- Test with real Claude Code SDK
- Test OpenAI client compatibility
- Test streaming and non-streaming responses

### Performance Tests
- Compare SDK vs CLI performance
- Test concurrent request handling
- Memory usage with session management

## Sub-Agent Opportunities

The following tasks can be effectively handled by sub-agents:

### High-Impact Sub-Agent Tasks:
1. **Authentication Enhancement** - Research and implement third-party provider support
2. **OpenAI Parameter Mapping** - Create comprehensive mapping between OpenAI and Claude Code parameters
3. **Error Handling Standardization** - Create error mapping and handling improvements
4. **Testing Suite Development** - Create comprehensive test suite for SDK integration

### Medium-Impact Sub-Agent Tasks:
5. **MCP Integration Research** - Investigate MCP integration patterns and best practices
6. **Session Storage Design** - Design session management and storage architecture
7. **Performance Optimization** - Analyze and optimize streaming performance
8. **Documentation Updates** - Update API documentation and examples

## Risk Mitigation

### Potential Issues:
1. **SDK Compatibility**: Claude Code SDK is relatively new (v0.0.14)
2. **Breaking Changes**: SDK may have breaking changes in future versions
3. **Performance**: SDK overhead vs direct CLI calls
4. **Feature Parity**: Some CLI features may not be available in SDK

### Mitigation Strategies:
1. Pin SDK version and test thoroughly
2. Implement fallback to CLI if needed
3. Performance benchmarking before/after
4. Gradual rollout with feature flags

## Success Criteria

### Phase 1 Success:
- ✅ SDK integration working
- ✅ Basic authentication working
- System prompts functional
- No regression in basic functionality

### Phase 2 Success:
- Session management working
- Tool configuration supported
- Improved metadata accuracy
- Enhanced streaming performance

### Phase 3 Success:
- Full OpenAI parameter compatibility
- Proper error handling
- Accurate cost tracking
- Production-ready stability

## Timeline Estimates

- **Phase 1**: 1-2 days (mostly complete)
- **Phase 2**: 2-3 days
- **Phase 3**: 1-2 days
- **Phase 4**: 3-5 days (optional)
- **Testing & Polish**: 1-2 days

**Total Estimated Time**: 8-14 days for full implementation