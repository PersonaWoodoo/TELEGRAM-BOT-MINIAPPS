import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# Токен бота
BOT_TOKEN = "8648458601:AAE-Rb0Y0ZAWuKJt3MZFwBzq0S9STRMBDSE"

# Ссылка на мини-приложение (замени на свою)
WEBAPP_URL = "https://personawoodoo.github.io/WILLD-GIFT/"

# Ссылка на канал
CHANNEL_URL = "https://t.me/VILLD_GIFT"

# Ссылка на поддержку
SUPPORT_URL = "https://t.me/debashev"

# Ссылка на фотку
PHOTO_URL = "https://i.supaimg.com/435c46f7-76b1-41ba-82e2-1f1a0a964f2c/bc2e341f-0e5f-4a83-80e6-d9801cc1025d.jpg"

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """Обработчик команды /start"""
    
    # Получаем реферальный код из ссылки (если есть)
    ref_code = message.text.split()[1] if len(message.text.split()) > 1 else None
    
    # Если есть реферальный код, добавляем его в URL
    webapp_url = WEBAPP_URL
    if ref_code:
        webapp_url = f"{WEBAPP_URL}?start={ref_code}"
    
    # Клавиатура с кнопками
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎁 ОТКРЫТЬ", web_app=WebAppInfo(url=webapp_url))],
        [
            InlineKeyboardButton(text="📢 КАНАЛ", url=CHANNEL_URL),
            InlineKeyboardButton(text="💬 ПОДДЕРЖКА", url=SUPPORT_URL)
        ]
    ])
    
    # Отправляем фото с кнопками
    await message.answer_photo(
        photo=PHOTO_URL,
        caption="🎁 БЕСПЛАТНОЕ ВРАЩЕНИЕ КАЖДЫЕ 24 ЧАСА!",
        reply_markup=keyboard
    )

@dp.message(Command("invite"))
async def cmd_invite(message: types.Message):
    """Реферальная ссылка"""
    
    bot_info = await bot.me()
    ref_link = f"https://t.me/{bot_info.username}?start={message.from_user.id}"
    
    # Текст для шеринга
    share_text = "🎁 БЕСПЛАТНОЕ ВРАЩЕНИЕ КАЖДЫЕ 24 ЧАСА!"
    share_url = f"https://t.me/share/url?url={ref_link}&text={share_text}"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📤 ПОДЕЛИТЬСЯ", url=share_url)]
    ])
    
    # Отправляем фото с реферальной ссылкой
    await message.answer_photo(
        photo=PHOTO_URL,
        caption=f"👥 Твоя реферальная ссылка:\n{ref_link}",
        reply_markup=keyboard
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
