from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import os

app = FastAPI()

# 🔐 Load API Key from environment
OPENROUTER_API_KEY = os.getenv("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")

if not OPENROUTER_API_KEY:
    raise RuntimeError("❌ OPENROUTER_API_KEY is not set")

# 🌐 Enable CORS (allow frontend access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🟢 Health Check
@app.get("/")
def home():
    return {"status": "AI Gateway Running 🚀"}

# 🤖 Chat Endpoint
@app.post("/chat")
async def chat(request: Request):
    try:
        body = await request.json()

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json=body,
            timeout=30
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.text
            )

        return response.json()

    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="Request timed out")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
