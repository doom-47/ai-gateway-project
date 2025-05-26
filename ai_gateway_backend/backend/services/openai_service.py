import openai
import os
from dotenv import load_dotenv
from openai import OpenAIError

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
USE_MOCK = os.getenv("USE_OPENAI_MOCK", "False").lower() == "true"

def generate_text_openai(prompt: str, model: str) -> tuple[str, int, int]:
    if USE_MOCK:
        return f"[MOCKED {model}] You said: {prompt}", 5, 10

    if not openai.api_key:
        raise RuntimeError("Missing OpenAI API key.")

    try:
        response = openai.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=100,
        )
        content = response.choices[0].message.content
        usage = getattr(response, "usage", None)
        input_tokens = usage.prompt_tokens if usage else 0
        output_tokens = usage.completion_tokens if usage else 0
        return content, input_tokens, output_tokens

    except OpenAIError as e:
        raise RuntimeError(f"OpenAI API call failed: {e}")
