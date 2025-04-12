from fastapi import FastAPI
from app.router import router

app = FastAPI(title="Universal Code Analyzer", version="1.0")
app.include_router(router)


# Synchronous Example
from mistralai import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.chat.complete(model="mistral-small-latest", messages=[
        {
            "content": "Who is the best French painter? Answer in one short sentence.",
            "role": "user",
        },
    ])

    # Handle response
    print(res)