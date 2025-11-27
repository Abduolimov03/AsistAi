# ai_handler.py
import os
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai
from memory import save_history

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("❌ GEMINI_API_KEY .env ichida topilmadi!")

genai.configure(api_key=GEMINI_API_KEY)
text_model = genai.GenerativeModel("models/gemini-flash-latest")

async def get_ai_text(prompt: str, user_id: int) -> str:
    try:
        response = text_model.generate_content(prompt)
        ai_text = response.text

        save_history(user_id, "user", prompt)
        save_history(user_id, "assistant", ai_text)

        return ai_text
    except Exception as e:
        return f"❌ AI xatolik berdi: {e}"

async def get_ai_image(prompt: str):
    return None

async def get_ai_audio(prompt: str):
    return None
