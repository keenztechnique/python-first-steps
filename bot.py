import os
import logging
import asyncio
import sqlite3
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv

TOKEN = "8946386750:AAHjAsdG8OpHSRdDsGOr2VX4CYMo0WU89tE"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Состояния для FSM
class BotStates(StatesGroup):
    waiting_for_quote_text = State()
    waiting_for_quote_author = State()
    waiting_for_search_query = State()

# Главное меню (с кнопкой статистики)
def get_main_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📌 Цитаты", callback_data="page_0"),
                InlineKeyboardButton(text="👤 Авторы", callback_data="show_authors")
            ],
            [
                InlineKeyboardButton(text="🔍 Поиск", callback_data="start_search"),
                InlineKeyboardButton(text="➕ Добавить цитату", callback_data="add_quote_start")
            ],
            [
                InlineKeyboardButton(text="📊 Статистика", callback_data="show_stats"),
                InlineKeyboardButton(text="ℹ️ О боте", callback_data="about_bot")
            ]
        ]
    )

# Клавиатура авторов
def get_authors_keyboard():
    conn = sqlite3.connect("quotes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT author FROM quotes LIMIT 6")
    authors = cursor.fetchall()
    conn.close()

    keyboard_buttons = []
    for (author,) in authors:
        keyboard_buttons.append([InlineKeyboardButton(text=author, callback_data=f"author_{author}")])
    
    keyboard_buttons.append([InlineKeyboardButton(text="⬅️ Главное меню", callback_data="back_to_main")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    welcome_text = (
        "Привет! Я продвинутый Telegram-бот для управления базой цитат.\n\n"
        "Выберите нужное действие в меню ниже:"
    )
    await message.answer(welcome_text, reply_markup=get_main_keyboard())

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    help_text = (
        "📖 **Справка по боту:**\n"
        "• Просмотр цитат с пагинацией\n"
        "• Фильтрация по авторам\n"
        "• Поиск по ключевым словам\n"
        "• Добавление новых цитат\n"
        "• Статистика базы данных"
    )
    await message.answer(help_text, reply_markup=get_main_keyboard())

@dp.message(Command("quotes"))
async def cmd_quotes(message: types.Message):
    await show_quotes_page(message, page=0, is_edit=False)

# --- Пагинация цитат ---
async def show_quotes_page(event, page: int, is_edit: bool = True):
    limit = 3
    offset = page * limit

    conn = sqlite3.connect("quotes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT author, text FROM quotes LIMIT ? OFFSET ?", (limit, offset))
    rows = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM quotes")
    total_count = cursor.fetchone()[0]
    conn.close()

    if not rows:
        text = "В базе данных пока нет цитат."
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="⬅️ Главное меню", callback_data="back_to_main")]])
    else:
        text = f"📌 **Цитаты (Страница {page + 1}):**\n\n"
        for idx, (author, text_val) in enumerate(rows, offset + 1):
            text += f"{idx}. *{author}*:\n{text_val}\n\n"

        nav_buttons = []
        if page > 0:
            nav_buttons.append(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"page_{page - 1}"))
        if offset + limit < total_count:
            nav_buttons.append(InlineKeyboardButton(text="Вперед ➡️", callback_data=f"page_{page + 1}"))

        keyboard_list = []
        if nav_buttons:
            keyboard_list.append(nav_buttons)
        keyboard_list.append([InlineKeyboardButton(text="⬅️ Главное меню", callback_data="back_to_main")])
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_list)

    if is_edit:
        await event.message.edit_text(text, parse_mode="Markdown", reply_markup=keyboard)
    else:
        await event.answer(text, parse_mode="Markdown", reply_markup=keyboard)

@dp.callback_query(F.data.startswith("page_"))
async def process_pagination(callback: types.CallbackQuery):
    page = int(callback.data.split("_")[1])
    await show_quotes_page(callback, page=page, is_edit=True)
    await callback.answer()

# --- Главное меню и общие кнопки ---
@dp.callback_query(F.data == "back_to_main")
async def process_back_to_main(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "📌 Главное меню. Выберите действие:",
        reply_markup=get_main_keyboard()
    )
    await callback.answer()

@dp.callback_query(F.data == "about_bot")
async def process_about(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "ℹ️ Этот бот управляет базой данных SQLite, поддерживает пагинацию, фильтрацию, поиск, добавление записей и сбор статистики.",
        reply_markup=get_main_keyboard()
    )
    await callback.answer()

# --- Статистика базы данных ---
@dp.callback_query(F.data == "show_stats")
async def process_show_stats(callback: types.CallbackQuery):
    try:
        conn = sqlite3.connect("quotes.db")
        cursor = conn.cursor()

        # Общее число цитат
        cursor.execute("SELECT COUNT(*) FROM quotes")
        total_quotes = cursor.fetchone()[0]

        # Количество уникальных авторов
        cursor.execute("SELECT COUNT(DISTINCT author) FROM quotes")
        total_authors = cursor.fetchone()[0]

        # Самая длинная цитата
        cursor.execute("SELECT author, text FROM quotes ORDER BY LENGTH(text) DESC LIMIT 1")
        longest = cursor.fetchone()

        conn.close()

        stats_text = (
            "📊 **Статистика базы данных:**\n\n"
            f"• Всего цитат: **{total_quotes}**\n"
            f"• Уникальных авторов: **{total_authors}**\n"
        )

        if longest:
            author_l, text_l = longest
            stats_text += f"\n🏆 **Самая длинная цитата** (*{author_l}*):\n_{text_l}_"

        await callback.message.edit_text(stats_text, parse_mode="Markdown", reply_markup=get_main_keyboard())
        await callback.answer()
    except Exception as e:
        await callback.message.answer(f"Ошибка при подсчете статистики: {e}", reply_markup=get_main_keyboard())

@dp.callback_query(F.data == "show_authors")
async def process_show_authors(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "📂 Выберите автора, чтобы посмотреть его цитаты:",
        reply_markup=get_authors_keyboard()
    )
    await callback.answer()

@dp.callback_query(F.data.startswith("author_"))
async def process_author_quotes(callback: types.CallbackQuery):
    selected_author = callback.data.replace("author_", "", 1)
    conn = sqlite3.connect("quotes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT text FROM quotes WHERE author = ? LIMIT 5", (selected_author,))
    rows = cursor.fetchall()
    conn.close()

    if rows:
        response = f"📌 **Цитаты автора {selected_author}:**\n\n"
        for idx, (text,) in enumerate(rows, 1):
            response += f"{idx}. {text}\n\n"
        await callback.message.edit_text(response, parse_mode="Markdown", reply_markup=get_authors_keyboard())
    else:
        await callback.message.edit_text(f"У автора {selected_author} нет цитат.", reply_markup=get_authors_keyboard())
    await callback.answer()

# --- Поиск по ключевому слову ---
@dp.callback_query(F.data == "start_search")
async def process_start_search(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("🔍 Введите слово или фразу для поиска по цитатам:")
    await state.set_state(BotStates.waiting_for_search_query)
    await callback.answer()

@dp.message(BotStates.waiting_for_search_query)
async def process_search_query(message: types.Message, state: FSMContext):
    query = message.text
    await state.clear()

    conn = sqlite3.connect("quotes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT author, text FROM quotes WHERE text LIKE ? LIMIT 5", (f"%{query}%",))
    rows = cursor.fetchall()
    conn.close()

    if rows:
        response = f"🔍 **Результаты поиска по запросу «{query}»:**\n\n"
        for idx, (author, text) in enumerate(rows, 1):
            response += f"{idx}. *{author}*:\n{text}\n\n"
        await message.answer(response, parse_mode="Markdown", reply_markup=get_main_keyboard())
    else:
        await message.answer(f"По запросу «{query}» ничего не найдено.", reply_markup=get_main_keyboard())

# --- Добавление цитаты через FSM ---
@dp.callback_query(F.data == "add_quote_start")
async def process_add_quote(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("✍️ Введите текст новой цитаты:")
    await state.set_state(BotStates.waiting_for_quote_text)
    await callback.answer()

@dp.message(BotStates.waiting_for_quote_text)
async def process_quote_text(message: types.Message, state: FSMContext):
    await state.update_data(quote_text=message.text)
    await message.answer("👤 Теперь введите автора этой цитаты:")
    await state.set_state(BotStates.waiting_for_quote_author)

@dp.message(BotStates.waiting_for_quote_author)
async def process_quote_author(message: types.Message, state: FSMContext):
    data = await state.get_data()
    quote_text = data.get("quote_text")
    quote_author = message.text

    try:
        conn = sqlite3.connect("quotes.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO quotes (author, text) VALUES (?, ?)", (quote_author, quote_text))
        conn.commit()
        conn.close()

        await message.answer(f"✅ Цитата успешно добавлена в базу данных!\n\n*{quote_author}*:\n{quote_text}", parse_mode="Markdown", reply_markup=get_main_keyboard())
    except Exception as e:
        await message.answer(f"Ошибка при сохранении: {e}", reply_markup=get_main_keyboard())
    
    await state.clear()

async def main():
    print("Бот запущен и ожидает сообщения...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())