from pydantic import BaseModel
from typing import Dict

class UsageSummary(BaseModel):
    total_requests: int
    total_input_tokens: int
    total_output_tokens: int
    estimated_total_cost_usd: float
    model_usage: Dict[str, Dict[str, int]]  # e.g., {"gpt-3.5-turbo": {"input_tokens": 1000, "output_tokens": 2000, "requests": 5}}