# Bot Implementation Plan

## Overview

This document outlines the development plan for the Telegram LMS Bot. The bot provides students with access to their lab assignments, scores, and course information through a conversational interface in Telegram.

## Architecture

The bot follows a layered architecture with clear separation of concerns:

1. **Entry Point** (`bot.py`) — Handles CLI arguments for test mode, initializes the Telegram bot for production
2. **Handlers** (`handlers/`) — Plain functions that process commands and return strings, independent of Telegram
3. **Services** (`services/`) — API clients for external services (LMS API, LLM API)
4. **Configuration** (`config.py`) — Centralized settings loaded from environment variables

## Development Phases

### Phase 1: Basic Command Handlers (Task 1)

Implement placeholder handlers for slash commands: `/start`, `/help`, `/health`, `/labs`, `/scores`. Create the `--test` mode that allows testing handlers without Telegram connectivity. This establishes the foundation for testable, isolated handler logic.

### Phase 2: LMS API Integration (Task 2)

Build an HTTP client service to communicate with the LMS backend. Implement Bearer token authentication using the API key from environment variables. Replace placeholder handlers with real API calls to fetch labs and scores. Handle errors gracefully when the API is unavailable.

### Phase 3: LLM-Powered Natural Language (Task 3)

Integrate an LLM client that enables the bot to understand plain text questions. Define tool descriptions for each handler so the LLM can route user intents to the appropriate function. Improve tool descriptions based on observed behavior rather than adding code-based routing fallbacks.

### Phase 4: Docker Deployment (Task 4)

Containerize the bot for deployment. Configure Docker networking so the bot container can reach the backend and LLM services using service names instead of localhost. Set up environment variable injection for secrets.

## Testing Strategy

- Unit tests for handlers (pure functions, easy to test)
- Integration tests for API clients (mocked responses)
- Manual testing via `--test` mode during development
- End-to-end testing in a private Telegram channel before deployment

## Security Considerations

- Never commit `.env.bot.secret` — it's gitignored
- Use environment variables for all secrets (bot token, API keys)
- Validate and sanitize user input before processing
- Handle API errors without exposing internal details to users
