from fastapi import APIRouter, Depends
from backend.db.database import get_connection
from backend.main import get_current_user, User
from backend.models.dashboard_model import UsageSummary

router = APIRouter()

def get_usage_summary_from_db(user: User):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT
                COUNT(*) as total_requests,
                SUM(input_tokens) as total_input_tokens,
                SUM(output_tokens) as total_output_tokens,
                model_name,
                SUM(CASE WHEN model_name = %s THEN input_tokens ELSE 0 END) as gpt_input,
                SUM(CASE WHEN model_name = %s THEN output_tokens ELSE 0 END) as gpt_output,
                SUM(CASE WHEN model_name LIKE 'claude%%' THEN input_tokens ELSE 0 END) as claude_input,
                SUM(CASE WHEN model_name LIKE 'claude%%' THEN output_tokens ELSE 0 END) as claude_output,
                SUM(CASE WHEN model_name LIKE 'llama%%' THEN input_tokens ELSE 0 END) as llama_input,
                SUM(CASE WHEN model_name LIKE 'llama%%' THEN output_tokens ELSE 0 END) as llama_output
            FROM usage_log
            WHERE user_id = %s
            GROUP BY model_name
            """,
            ("gpt-3.5-turbo", "gpt-3.5-turbo", user.id)
        )
        all_results = cursor.fetchall()

        total_requests = 0
        total_input_tokens = 0
        total_output_tokens = 0
        model_usage = {'gpt': {'input_tokens': 0, 'output_tokens': 0, 'requests': 0},
                       'claude': {'input_tokens': 0, 'output_tokens': 0, 'requests': 0},
                       'llama': {'input_tokens': 0, 'output_tokens': 0, 'requests': 0}}

        for row in all_results:
            total_requests += row.get('total_requests', 0) or 0
            total_input_tokens += row.get('total_input_tokens', 0) or 0
            total_output_tokens += row.get('total_output_tokens', 0) or 0
            model_name = row.get('model_name', '')
            if 'gpt' in model_name:
                model_usage['gpt']['input_tokens'] += row.get('gpt_input', 0) or 0
                model_usage['gpt']['output_tokens'] += row.get('gpt_output', 0) or 0
                # Increment request count per model if needed
            elif 'claude' in model_name:
                model_usage['claude']['input_tokens'] += row.get('claude_input', 0) or 0
                model_usage['claude']['output_tokens'] += row.get('claude_output', 0) or 0
            elif 'llama' in model_name:
                model_usage['llama']['input_tokens'] += row.get('llama_input', 0) or 0
                model_usage['llama']['output_tokens'] += row.get('llama_output', 0) or 0
            # Increment request count per model if needed

        estimated_total_cost_usd = 0.000005 * (float(total_input_tokens) + float(total_output_tokens))

        return UsageSummary(
            total_requests=total_requests,
            total_input_tokens=total_input_tokens,
            total_output_tokens=total_output_tokens,
            estimated_total_cost_usd=estimated_total_cost_usd,
            model_usage=model_usage
        )
    finally:
        cursor.close()
        conn.close()

@router.get("/usage/summary", response_model=UsageSummary, dependencies=[Depends(get_current_user)])
def get_usage_summary(current_user: User = Depends(get_current_user)):
    summary = get_usage_summary_from_db(current_user)
    return summary