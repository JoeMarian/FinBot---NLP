
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.chatbot import router as chatbot_router
from api.finance import router as finance_router

app = FastAPI(title="Knowledge-Aware Personal Finance Chatbot", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chatbot_router, prefix="/api")
app.include_router(finance_router, prefix="/api")

@app.get("/health")
def health():
    return {"status": "ok"}
