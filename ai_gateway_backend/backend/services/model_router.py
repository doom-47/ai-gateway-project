import os
from backend.services.openai_service import generate_text_openai
from backend.services.anthropic_service import generate_text_anthropic
from backend.services.llama_service import generate_text_llama  # Import the LLaMA service function
import unicodedata

def clean_string(s: str) -> str:
    s = s.lower()
    s = s.strip()  # Remove leading/trailing whitespace
    s = "".join(ch for ch in s if ch.isprintable())  # Remove non-printable chars
    s = unicodedata.normalize('NFKC', s)  # Normalize Unicode
    return s

def route_model(model_name: str, prompt: str):
    print(f"Original model_name: {model_name}")  # Debug
    model_name = clean_string(model_name)
    print(f"Cleaned model_name: {model_name}")  # Debug

    response = ""
    input_tokens = 0
    output_tokens = 0

    if model_name.startswith("gpt"):
        response, input_tokens, output_tokens = generate_text_openai(prompt, model_name)
    elif model_name.startswith("claude"):
        response, input_tokens, output_tokens = generate_text_anthropic(prompt, model_name)
    elif "llama" in model_name:  # Check if "llama" is a substring
        print("Routing to LLaMA")  # Debug
        response, input_tokens, output_tokens = generate_text_llama(prompt, model_name)
    else:
        raise ValueError(f"Unsupported model: {model_name}")

    # REMOVE THE ESTIMATED_COST_USD CALCULATION AND RETURN FROM HERE
    # estimated_cost_usd = 0.000005 * (input_tokens + output_tokens) if input_tokens > 0 or output_tokens > 0 else 0.0

    return response, input_tokens, output_tokens # ONLY RETURN 3 VALUES