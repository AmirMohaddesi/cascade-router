import os
from openai import OpenAI

# We point the official OpenAI SDK to our local C++ proxy
client = OpenAI(
    base_url="http://localhost:8000/v1", 
    api_key=os.environ.get("OPENAI_API_KEY", "sk-test-key")
)

print("Sending request through Cascade...")
try:
    response = client.chat.completions.create(
        model="cascade-auto", # The proxy intercepts this
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Write a one-line python function to reverse a string."}
        ]
    )
    print("\n--- Upstream Response ---")
    print(response.choices[0].message.content)
except Exception as e:
    print(f"\nError: {e}")
