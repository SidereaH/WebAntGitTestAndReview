import os
from mistralai import Mistral

model = "mistral-small-latest"

def mistral_chat(prompt: str) -> str:
    with Mistral(
        api_key=os.getenv("MISTRAL_API_KEY", ""),
    ) as client:
        response = client.chat.complete(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content