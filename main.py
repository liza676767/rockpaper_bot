import os
import asyncio
import random
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiohttp import web

# Отримуємо токен
TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()
choices = ["Камінь", "Ножиці", "Папір"]

# --- Секція для обходу помилки Render ---
async def handle(request):
    return web.Response(text="Бот працює!")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    # Render автоматично дає порт у змінну PORT
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
# ----------------------------------------

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    for choice in choices:
        builder.add(types.KeyboardButton(text=choice))
    await message.answer("Привіт! Граємо? Вибирай:", reply_markup=builder.as_markup(resize_keyboard=True))

@dp.message(lambda message: message.text in choices)
async def play_game(message: types.Message):
    user_choice = message.text
    bot_choice = random.choice(choices)
    rules = {"Камінь": "Ножиці", "Ножиці": "Папір", "Папір": "Камінь"}
    if user_choice == bot_choice:
        result = "Нічия! 🤝"
    elif rules[user_choice] == bot_choice:
        result = "Ти переміг! 🎉"
    else:
        result = "Я переміг! 🤖"
    await message.answer(f"Мій вибір: {bot_choice}\n{result}")

async def main():
    # Запускаємо фейковий веб-сервер для Render
    asyncio.create_task(start_web_server())
    # Запускаємо бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
