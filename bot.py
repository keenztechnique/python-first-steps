import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import sqlite3

# Ваш токен от BotFather
TOKEN = "8946386750:AAHjAsdG8OpHSRdDsGOr2VX4CYMo0WU89tE"

# Настраиваем логирование
logging.basicConfig(level=logging.INFO)

# Инициализируем бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
  """Обработчик команды /start"""
  welcome_text = (
      "Привет! Я твой профессиональный Telegram-бот для управления"
      " скрейпером.\n\nДоступные команды:\n/quotes — Посмотреть последние цитаты"
      " из базы данных\n/help — Справка"
  )
  await message.answer(welcome_text)

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
  """Обработчик команды /help"""
  help_text = (
      "Я умею подключаться к базе данных SQLite (`quotes.db`) и выдавать"
      " собранные цитаты прямо в чат!"
  )
  await message.answer(help_text)

@dp.message(Command("quotes"))
async def cmd_quotes(message: types.Message):
  """Обработчик команды /quotes: читает данные из SQLite и отправляет в чат"""
  try:
    conn = sqlite3.connect("quotes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT author, text FROM quotes LIMIT 5")
    rows = cursor.fetchall()
    conn.close()

    if rows:
      response = "📌 **Последние цитаты из базы данных:**\n\n"
      for idx, (author, text) in enumerate(rows, 1):
        response += f"{idx}. *{author}*:\n{text}\n\n"
      await message.answer(response, parse_mode="Markdown")
    else:
      await message.answer(
          "В базе данных пока нет цитат. Сначала запустите `main.py` для"
          " сбора!"
      )
  except Exception as e:
    await message.answer(f"Ошибка при чтении базы данных: {e}")

async def main():
  print("Бот запущен и ожидает сообщения...")
  await dp.start_polling(bot)

if __name__ == "__main__":
  asyncio.run(main())