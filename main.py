import os
import random
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# Отримуємо токен зі змінних оточення Render
TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

choices = ["Камінь", "Ножиці", "Папір"]

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*(types.KeyboardButton(choice) for choice in choices))
    await message.reply("Привіт! Давай зіграємо у 'Камінь, ножиці, папір'. Вибирай свій хід:", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text in choices)
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
        
    await message.reply(f"Мій вибір: {bot_choice}\n{result}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)