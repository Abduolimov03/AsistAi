import os
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai
from memory import save_history
import base64

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("❌ GEMINI_API_KEY .env ichida topilmadi!")

genai.configure(api_key=GEMINI_API_KEY)

text_model = genai.GenerativeModel("models/gemini-flash-latest")
image_model = genai.GenerativeModel("models/gemini-image-latest")
audio_model = genai.GenerativeModel("models/gemini-tts-latest")


async def get_ai_text(prompt: str, user_id: int) -> str:
    try:
        response = text_model.generate_content(prompt)
        ai_text = response.text

        save_history(user_id, prompt, ai_text)
        return ai_text
    except Exception as e:
        return f"❌ AI xatolik berdi: {e}"


async def get_ai_image(prompt: str):
    try:
        response = image_model.generate_content(prompt)
        if getattr(response, "image_base64", None):
            img_bytes = base64.b64decode(response.image_base64)
            return img_bytes
        return getattr(response, "image_url", None)
    except Exception:
        return None


async def get_ai_audio(prompt: str):
    try:
        response = audio_model.generate_content(prompt)
        if getattr(response, "audio_base64", None):
            audio_bytes = base64.b64decode(response.audio_base64)
            return audio_bytes
        return getattr(response, "audio_url", None)
    except Exception:
        return None
