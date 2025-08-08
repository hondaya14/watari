# Watari Project Overview

Watari is a tool integration project that provides various utilities including Google Calendar integration and Discord bot functionality. The name "Watari" appears to be inspired by the character from Death Note.

## Purpose
- Integrated tools for various services
- Google Calendar management (get events, create events, list calendars)
- Discord bot functionality
- LLM integration for chat functionality

## Tech Stack
- **Language**: Python 3.13+
- **Package Management**: uv (with mise for Python version management)
- **Key Dependencies**:
  - google-api-python-client (>=2.176.0)
  - google-auth-httplib2 (>=0.2.0) 
  - google-auth-oauthlib (>=1.2.2)
  - discord (>=2.3.2)
  - llm (>=0.26)

## Project Structure
```
watari/
├── tools/
│   ├── google_calendar.py  # Google Calendar API integration
│   └── hello_world.py      # Basic tool example
├── discord/
│   └── discord_bot.py      # Discord bot implementation
├── requirements.txt        # Locked dependencies
├── pyproject.toml         # Project configuration
├── mise.toml              # Python version and task management
└── uv.lock               # UV lockfile
```

## Configuration
- Uses environment variables for sensitive data (Discord token, etc.)
- Credential files (credential.json, token.json) are gitignored
- Environment example provided in .env.example