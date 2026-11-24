from ollama import chat

response = chat(
    model="qwen3:4b",
    messages=[
        {"role": "user", "content": "Hi"}
    ],
    think=False
)

print("CONTENT:", repr(response.message.content))
print("THINKING:", repr(response.message.thinking))