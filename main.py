from fastapi import FastAPI
from pydantic import BaseModel
from ai_chat import AgeBasedChatbot
from fastapi.middleware.cors import CORSMiddleware




# -------------------------------
# Config
# -------------------------------
FIXED_AGE = 20  # Temporary age until ML model sends real one
API_KEY = "AIzaSyC7Vhu1MVBdg13Rjib8I4K7JBnA6aaw52M"

bot = AgeBasedChatbot(age=FIXED_AGE, api_key=API_KEY)

# -------------------------------
# FastAPI App
# -------------------------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 👈 You can restrict to ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat_endpoint(req: ChatRequest):
    response = bot.chat(req.message)
    return {"reply": response}
