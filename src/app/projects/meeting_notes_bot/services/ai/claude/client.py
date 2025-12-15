import os
import anthropic

CLAUDE_API_KEY = os.getenv('ANTHROPIC_API_KEY')

if not CLAUDE_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY environment variable not set")

client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)