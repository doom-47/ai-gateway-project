import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()
LLAMA_API_KEY = os.getenv("LLAMA_API_KEY")
# Using OpenRouter's API endpoint for LLaMA models
LLAMA_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# You can add a specific mock flag for LLaMA if you want more granular control,
# but for now, it falls back to mock if LLAMA_API_KEY is missing.
USE_LLAMA_MOCK = os.getenv("USE_LLAMA_MOCK", "False").lower() == "true"


def generate_text_llama(prompt: str, model: str) -> tuple[str, int, int]:
    """
    Generates text using a LLaMA model via OpenRouter API or returns a mock response.
    """
    if USE_LLAMA_MOCK or not LLAMA_API_KEY:
        # Returns a mocked response if USE_LLAMA_MOCK is True or API key is missing
        return f"[MOCK] LLaMA response from {model} for prompt: '{prompt}'", len(prompt.split()), 20

    headers = {
        "Authorization": f"Bearer {LLAMA_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model, # e.g., "meta-llama/llama-3-8b-instruct" or "meta-llama/llama-4-maverick"
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 100, # Adjust as needed
        "temperature": 0.7 # Adjust creativity
    }

    try:
        response = requests.post(LLAMA_API_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

        result = response.json()
        content = result["choices"][0]["message"]["content"]
        usage = result.get("usage", {})
        input_tokens = usage.get("prompt_tokens", 0)
        output_tokens = usage.get("completion_tokens", 0)

        return content, input_tokens, output_tokens

    except requests.exceptions.RequestException as e:
        # Handles network errors, bad HTTP responses, etc.
        print(f"LLaMA API Request Error: {e}")
        return f"[LLaMA API Error]: {e}", len(prompt.split()), 0 # Fallback token count
    except json.JSONDecodeError as e:
        # Handles cases where the response is not valid JSON
        print(f"LLaMA API JSON Decode Error: {e}")
        return f"[LLaMA API Error]: Invalid JSON response: {e}", len(prompt.split()), 0
    except KeyError as e:
        # Handles cases where expected keys are missing in the JSON response
        print(f"LLaMA API Response Structure Error: Missing key {e}")
        return f"[LLaMA API Error]: Unexpected response structure (missing key: {e})", len(prompt.split()), 0
    except Exception as e:
        # Catch any other unexpected errors
        print(f"An unexpected error occurred in LLaMA service: {e}")
        return f"[LLaMA API Error]: An unexpected error occurred: {e}", len(prompt.split()), 0