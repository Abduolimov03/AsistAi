import os
import io
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from ai_handler import get_ai_text, get_ai_image, get_ai_audio
from memory import clear_history

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not BOT_TOKEN or not GEMINI_API_KEY:
    raise RuntimeError("❌ BOT_TOKEN yoki GEMINI_API_KEY topilmadi!")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


main_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="❌ Clear History", callback_data="clear")],
    [InlineKeyboardButton(text="ℹ️ About", callback_data="about")]
])

reply_type_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📝 Text", callback_data="type_text"),
     InlineKeyboardButton(text="🖼 Image", callback_data="type_image"),
     InlineKeyboardButton(text="🔊 Audio", callback_data="type_audio")]
])

user_reply_type = {}
MAX_MSG_LEN = 4000

async def send_long_text(message_obj, text, reply_markup=None):
    for i in range(0, len(text), MAX_MSG_LEN):
        chunk = text[i:i + MAX_MSG_LEN]
        if i == 0:
            await message_obj.edit_text(chunk, reply_markup=reply_markup)
        else:
            await message_obj.answer(chunk)

@dp.message(Command(commands=["start"]))
async def start(message: types.Message):
    await message.answer(
        "👋 Salom! Men Gemini AI botman.\n"
        "Savolingizni yuboring va javob turini tanlang!",
        reply_markup=reply_type_menu
    )

@dp.callback_query(lambda c: c.data == "clear")
async def clear_callback(callback: types.CallbackQuery):
    clear_history(callback.from_user.id)
    await callback.answer("✅ Tarix tozalandi!")

@dp.callback_query(lambda c: c.data == "about")
async def about_callback(callback: types.CallbackQuery):
    await callback.answer("🤖 Professional Gemini AI bot\nMultimodal: text, image, audio", show_alert=True)

@dp.callback_query(lambda c: c.data.startswith("type_"))
async def reply_type_callback(callback: types.CallbackQuery):
    type_selected = callback.data.split("_")[1]
    user_reply_type[callback.from_user.id] = type_selected
    await callback.answer(f"✅ Javob turi tanlandi: {type_selected}")

@dp.message()
async def handle_message(message: types.Message):
    user_text = message.text
    reply_type = user_reply_type.get(message.from_user.id, "text")
    typing = await message.answer("🤖 AI javobini tayyorlamoqda...")

    try:
        if reply_type == "text":
            ai_text = await get_ai_text(user_text, message.from_user.id)
            await send_long_text(typing, ai_text, reply_markup=main_menu)

        elif reply_type == "image":
            ai_image = await get_ai_image(user_text)
            if ai_image:
                await typing.delete()
                if isinstance(ai_image, bytes):
                    bio = io.BytesIO(ai_image)
                    bio.name = "image.png"
                    await message.answer_photo(photo=bio, caption="Rasm tayyor", reply_markup=main_menu)
                else:
                    await message.answer_photo(photo=ai_image, caption="Rasm tayyor", reply_markup=main_menu)
            else:
                await typing.edit_text("❌ Rasm hosil bo‘lmadi", reply_markup=main_menu)

        elif reply_type == "audio":
            ai_audio = await get_ai_audio(user_text)
            if ai_audio:
                await typing.delete()
                if isinstance(ai_audio, bytes):
                    bio = io.BytesIO(ai_audio)
                    bio.name = "audio.mp3"
                    await message.answer_audio(audio=bio, caption="Audio tayyor", reply_markup=main_menu)
                else:
                    await message.answer_audio(audio=ai_audio, caption="Audio tayyor", reply_markup=main_menu)
            else:
                await typing.edit_text("❌ Audio hosil bo‘lmadi", reply_markup=main_menu)

    except Exception as e:
        await typing.edit_text(f"❌ Xatolik: {e}", reply_markup=main_menu)

if __name__ == "__main__":
    print("[DEBUG] Bot ishga tushmoqda...")
    asyncio.run(dp.start_polling(bot))
