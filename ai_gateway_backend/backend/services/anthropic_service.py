import os
from dotenv import load_dotenv
import anthropic

load_dotenv()
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

def generate_text_anthropic(prompt: str, model: str) -> tuple[str, int, int]:
    if not ANTHROPIC_API_KEY:
        return "[Mock] Anthropic API key missing or no credits.", len(prompt.split()), 6

    try:
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        response = client.messages.create(
            model=model,
            max_tokens=100,
            temperature=0.7,
            messages=[{"role": "user", "content": prompt}]
        )
        content = response.content[0].text
        input_tokens = response.usage.input_tokens
        output_tokens = response.usage.output_tokens
        return content, input_tokens, output_tokens
    except Exception as e:
        # Fallback in case Anthropic fails
        return f"[Mock] Anthropic error: {e}", len(prompt.split()), 6
