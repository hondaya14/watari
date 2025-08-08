# Task Completion Checklist

When completing development tasks in Watari:

## No Explicit Testing/Linting Commands Found
- No pytest, ruff, black, or other linting/testing commands found in pyproject.toml or mise.toml
- No pre-commit hooks or CI configuration detected
- Manual testing may be required for Google Calendar and Discord functionality

## Before Committing
1. Ensure sensitive data is not included (tokens, credentials)
2. Update requirements.txt if dependencies changed: `mise run export`
3. Test functionality manually:
   - For Google Calendar: Test authentication flow and API calls
   - For Discord bot: Test bot responses and event handling
   - For LLM integration: Test function calling with tools

## Environment Requirements
- Ensure `.env` file is properly configured (copy from `.env.example`)
- Verify Google Calendar credentials are in place (`credential.json`)
- Check Discord bot token is set in environment

## Git Practices
- Credential files (`credential.json`, `token.json`) are properly gitignored
- Environment files (`.env`) are not committed