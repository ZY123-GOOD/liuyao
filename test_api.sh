curl http://localhost:8000/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{
        "messages": [
            {"role": "system", "content": "你是一个幽默的助手。"},
            {"role": "user", "content": "Qwen3 比 Qwen2 强在哪里？"}
        ],
        "temperature": 0.7
    }'