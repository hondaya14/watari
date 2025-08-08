# Code Style and Conventions

## Python Style
Based on analysis of existing code:

### Type Hints
- Uses type hints extensively
- Example: `creds: typing.Union[Credentials, None] = None`
- Imports typing module for complex types

### Docstrings
- Uses triple-quoted docstrings for functions
- Example: `"""Authenticate and return the Google Calendar API service."""`

### Import Organization
- Standard library imports first
- Third-party imports second
- Local imports last
- Specific imports from modules (e.g., `from google.auth.transport.requests import Request`)

### Naming Conventions
- snake_case for functions and variables
- UPPER_CASE for constants (e.g., `SCOPES`, `TOKEN`)
- Descriptive function names (e.g., `authenticate`, `get_schedule`, `create_event`)

### Code Patterns
- Environment variable usage with `os.getenv()`
- Credential management with file-based tokens
- Error handling for expired credentials with refresh logic
- Use of context managers for file operations

### Project-Specific Patterns
- Google API authentication follows OAuth2 flow pattern
- Credentials stored in `token.json` and `credential.json` files
- Logging using standard logging module
- Discord bot uses discord.py event-driven architecture