ro:ai_gateway_backend yash$ curl -X POST http://127.0.0.1:8000/generate \
>   -H "Content-Type: application/json" \
>   -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0dXNlciIsImV4cCI6MTc0ODEwODQ2MH0.Xj2BC3RBSrB4r-A-YmlKW-Z-WBAlwmEBK5j-JYKJofs" \
>   -d '{
>     "prompt": "Explain quantum computing in simple terms.",
>     "model_name": "gpt-3.5-turbo"
> }'
{"response":"[MOCK] Response from gpt-3.5-turbo for prompt: 'Explain quantum computing in simple terms.'","input_tokens":10,"output_tokens":20,"estimated_cost_usd":5.5e-05}venvYASHs-MacBook-Pro:ai_gateway_backend yash$ 
{
  "user_id": "user_123",
  "prompt": "Summarize the benefits of renewable energy.",
  "model_name": "gpt-4"
}
user_123
curl -X POST http://127.0.0.1:8000/generate \
-H "Content-Type: application/json" \
-d '{
  "user_id": "test123",
  "prompt": "What is the capital of France?",
  "model_name": "gpt-3.5-turbo"
}'
uvicorn backend.main:app --reload
  getting token
  curl -X POST http://127.0.0.1:8000/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=testpass"
  using it
  curl -X POST http://127.0.0.1:8000/generate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0dXNlciIsImV4cCI6MTc0ODE1NzU2MX0.ZVGL3CuxlyujviaoBdqWeKxRUUJRU1PifT6j2W6Z60g" \
  -d '{
    "prompt": "Explain quantum computing in simple terms.",
    "model_name": "gpt-3.5-turbo"
}'

llama
curl -X POST http://127.0.0.1:8000/generate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0dXNlciIsImV4cCI6MTc0ODI1MjQ5MX0.vfsc8RlIB_xeEI5po_ZG6c-y4-fE702hbE3R1Sr9w7c" \
  -d '{
    "prompt": "Summarize the history of AI.",
    "model_name": "llama2-7b-chat"
}'
antropic
curl -X POST http://127.0.0.1:8000/generate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0dXNlciIsImV4cCI6MTc0ODE1NzU2MX0.ZVGL3CuxlyujviaoBdqWeKxRUUJRU1PifT6j2W6Z60g" \
  -d '{
    "prompt": "What is the meaning of life?",
    "model_name": "claude-3-opus"
}'

-------------------------------------------------
{"detail":"Unsupported model: meta-llama/llama-3-8b-instruct"}(venv) venvYASHs-MacBook-Pro:ai_gateway_backend yash$ curl -X POST http://127.0.0.1:8000/token \
>   -H "Content-Type: application/x-www-form-urlencoded" \
>   -d "username=testuser&password=testpass"
{"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0dXNlciIsImV4cCI6MTc0ODE2MTM0NH0.jBrzWNJNIMOecVyA2UBViIzYzssNYBF7_ij-uBBoH8M","token_type":"bearer"}(venv) venvYASHs-MacBook-Pro:ai_gateway_backend yash$ curl -X POST http://127.0.0.1:8000/generate \
>   -H "Content-Type: application/json" \
>   -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0dXNlciIsImV4cCI6MTc0ODE2MTM0NH0.jBrzWNJNIMOecVyA2UBViIzYzssNYBF7_ij-uBBoH8M" \
>   -d '{
>     "prompt": "Tell me a fun fact.",
>     "model_name": "gpt-3.5-turbo"
> }'
{"detail":"Unexpected error: OpenAI API call failed: Error code: 429 - {'error': {'message': 'You exceeded your current quota, please check your plan and billing details. For more information on this error, read the docs: https://platform.openai.com/docs/guides/error-codes/api-errors.', 'type': 'insufficient_quota', 'param': None, 'code': 'insufficient_quota'}}"}(venv) venvYASHs-MacBook-Pro:ai_gateway_backend yash$ curl -X POST http://127.0.0.1:8000/generate \
>   -H "Content-Type: application/json" \
>   -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0dXNlciIsImV4cCI6MTc0ODE2MTM0NH0.jBrzWNJNIMOecVyA2UBViIzYzssNYBF7_ij-uBBoH8M" \
>   -d '{
>     "prompt": "Explain the concept of entropy briefly.",
>     "model_name": "claude-3-opus"
> }'
{"response":"[Mock] Anthropic error: Error code: 400 - {'type': 'error', 'error': {'type': 'invalid_request_error', 'message': 'Your credit balance is too low to access the Anthropic API. Please go to Plans & Billing to upgrade or purchase credits.'}}","input_tokens":6,"output_tokens":6,"estimated_cost_usd":6.000000000000001e-05}(venv) venvYASHs-MacBook-Pro:ai_gateway_backend yash$ curl -X POST http://127.0.0.1:8000/generate \
>   -H "Content-Type: application/json" \
>   -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0dXNlciIsImV4cCI6MTc0ODE2MTM0NH0.jBrzWNJNIMOecVyA2UBViIzYzssNYBF7_ij-uBBoH8M" \
>   -d '{
>     "prompt": "What are the main differences between a cat and a dog?",
>     "model_name": "meta-llama/llama-3-8b-instruct"
> }'
{"response":"While both cats and dogs are popular household pets, they have many differences in terms of their behavior, physiology, and characteristics. Here are some of the main differences:\n\n1. **Body Structure**: Cats are generally smaller and more agile than dogs. They have a slender body, shorter legs, and a longer tail. Dogs, on the other hand, come in a wide range of sizes, from small to large, with longer legs and a shorter tail.\n2. **Diet**: Cats are oblig","input_tokens":22,"output_tokens":100,"estimated_cost_usd":0.0006100000000000001}(venv) venvYASHs-MacBook-Pro:ai_gateway_backend yash$ 
------
uvicorn backend.main:app --reload
curl -X POST http://127.0.0.1:8000/register \
    -H "Content-Type: application/json" \
    -d '{"username": "newuser", "email": "new@example.com", "password": "securepass"}'

    curl -X POST http://127.0.0.1:8000/token \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=testuser&password=testpass"

    ACCESS_TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0dXNlciIsImV4cCI6MTc0ODI1MjQ5MX0.vfsc8RlIB_xeEI5po_ZG6c-y4-fE702hbE3R1Sr9w7c"
curl -X POST http://127.0.0.1:8000/generate \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -d '{"prompt": "Write a short poem about a cat.", "model_name": "llama-2-7b-chat-hf"}'

logs
    ACCESS_TOKEN="<YOUR_ACCESS_TOKEN>"
curl -X GET http://127.0.0.1:8000/usage \
    -H "Authorization: Bearer $ACCESS_TOKEN"
  
summary
ACCESS_TOKEN="<YOUR_ACCESS_TOKEN>"
curl -X GET http://127.0.0.1:8000/usage \
    -H "Authorization: Bearer $ACCESS_TOKEN"
    