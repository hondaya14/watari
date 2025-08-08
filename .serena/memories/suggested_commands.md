# Watari - Suggested Commands

## Development Commands

### Package Management
- `uv sync` - Sync dependencies
- `uv add <package>` - Add new dependency
- `uv export` - Export dependencies
- `uv export --format requirements-txt --locked -o requirements.txt` - Export to requirements.txt

### Export Task (defined in mise.toml)
- `mise run export` - Run export task (exports dependencies in multiple formats)

### Running the Project
Based on README.md examples:

```bash
# Basic LLM interaction
llm --key $LLM_API_KEY -m $LLM_MODEL "Hello."

# Chat with function calling
llm chat --key $LLM_API_KEY -m $LLM_MODEL --functions tools/{tools}.py --td
```

### Environment Setup
- Copy `.env.example` to `.env` and configure required variables
- Set up Google Calendar credentials in `credential.json` (not tracked in git)
- Set `DISCORD_BOT_TOKEN` in environment

### System Commands (Darwin/macOS)
Standard Unix commands are available:
- `ls`, `cd`, `grep`, `find`
- `git` for version control