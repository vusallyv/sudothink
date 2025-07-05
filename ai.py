import os
import sys
from openai import OpenAI
from openai import AuthenticationError

query = " ".join(sys.argv[1:])

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("❌ OPENAI_API_KEY not set. Please export it.")
    sys.exit(1)

client = OpenAI(api_key=api_key)

try:
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful Linux shell assistant. Only return valid shell commands, nothing else."},
            {"role": "user", "content": f"Convert this to a bash command:\n{query}"}
        ],
        temperature=0,
        max_tokens=100
    )
    print(response.choices[0].message.content.strip())
except AuthenticationError:
    print("❌ Invalid OpenAI API key. Please check OPENAI_API_KEY.")
