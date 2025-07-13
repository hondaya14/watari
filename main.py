import llm
import os
from typing import Optional

def get_env(name: str, default: Optional[str] = None, required: bool = False) -> str:
    value = os.getenv(name, default)
    if required and value is None:
        raise ValueError(f"Required environment variable '{name}' is not set")
    return value

def upper(text: str) -> str:
    """Convert text to uppercase."""
    return text.upper()

def count_char(text: str, character: str) -> int:
    """Count the number of occurrences of a character in a word."""
    return text.count(character)

@llm.hookimpl
def register_tools(register):
    register(upper)
    # Here the name= argument is used to specify a different name for the tool:
    register(count_char, name="count_character_in_word")

def main():
    model_name = get_env("LLM_MODEL", default="gemini/gemini-2.5-flash", required=True)
    print(f"Using model: {model_name}")
    
    model = llm.get_model(model_name)
    response = model.prompt("Convert panda to upper", tools=[upper])
    tool_calls = response.tool_calls()
    # [ToolCall(name='upper', arguments={'text': 'panda'}, tool_call_id='...')]

if __name__ == "__main__":
    main()
