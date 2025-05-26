from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.db.database import get_connection
from backend.services.model_router import route_model
from backend.models.usage_model import UsageLog

router = APIRouter()

class RequestPayload(BaseModel):
    user_id: str
    prompt: str
    model_name: str

def log_usage(user_id: str, model_name: str, input_tokens: int, output_tokens: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO usage_log (user_id, model_name, input_tokens, output_tokens, timestamp)
        VALUES (%s, %s, %s, %s, NOW())
        """,
        (user_id, model_name, input_tokens, output_tokens)
    )
    conn.commit()
    cursor.close()
    conn.close()

@router.post("/generate")
async def generate(payload: RequestPayload):
    try:
        # route_model now returns 4 values
        response, input_tokens, output_tokens, estimated_cost_usd = route_model(payload.model_name, payload.prompt)

        # Log usage
        log_usage(payload.user_id, payload.model_name, input_tokens, output_tokens)

        return {
            "response": response,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "estimated_cost_usd": estimated_cost_usd,
            "model": payload.model_name
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")

@router.get("/usage/{user_id}", response_model=list[UsageLog])
def get_usage(user_id: str):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT id, user_id, model_name, input_tokens, output_tokens, timestamp 
        FROM usage_log WHERE user_id = %s ORDER BY timestamp DESC
        """,
        (user_id,)
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows
