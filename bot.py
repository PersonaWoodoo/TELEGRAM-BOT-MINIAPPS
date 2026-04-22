import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# Токен бота
BOT_TOKEN = "8648458601:AAE-Rb0Y0ZAWuKJt3MZFwBzq0S9STRMBDSE"

# Ссылка на мини-приложение (замени на свою, когда зальёшь на GitHub Pages)
WEBAPP_URL = "https://personawoodoo.github.io/WILLD-GIFT/"

# Ссылка на сообщество
COMMUNITY_URL = "https://t.me/VILLD_GIFT"

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
    
    # Создаём клавиатуру с кнопками
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎁 ОТКРЫТЬ БЕСПЛАТНЫЙ КЕЙС", web_app=WebAppInfo(url=webapp_url))],
        [InlineKeyboardButton(text="👥 ПРИГЛАСИТЬ ДРУЗЕЙ", callback_data="invite")],
        [
            InlineKeyboardButton(text="📋 Пользовательское соглашение", url="https://t.me/durov"),
            InlineKeyboardButton(text="💬 Поддержка", url="https://t.me/debashev")
        ],
        [InlineKeyboardButton(text="🌟 Присоединиться к сообществу", url=COMMUNITY_URL)]
    ])
    
    # Приветственное сообщение (если нет фото, можно просто текст)
    welcome_text = (
        f"🎁 <b>VILLD GIFT</b>\n"
        f"👥 17,812 пользователей\n\n"
        f"Реклама VILLD GIFT\n"
        f"Что это?\n"
        f"Ежедневный бесплатный кейс каждые 24 часа. Внутри случайный подарок 🎁\n\n"
        f"Try your luck in daily gift raffles at @VilldGiftBot\n"
        f"Open cases and win amazing prizes every day!\n\n"
        f"🕐 {message.date.strftime('%H:%M')}"
    )
    
    await message.answer(
        welcome_text,
        parse_mode="HTML",
        reply_markup=keyboard
    )

@dp.callback_query(lambda c: c.data == "invite")
async def process_invite(callback: types.CallbackQuery):
    """Обработчик кнопки ПРИГЛАСИТЬ ДРУЗЕЙ"""
    
    bot_info = await bot.me()
    ref_link = f"https://t.me/{bot_info.username}?start={callback.from_user.id}"
    
    # Текст для репоста
    share_text = (
        "🎁 Открывай Free Box в VILLD GIFT и забирай свои NFT-подарки!\n\n"
        "Это на 100% бесплатно, можешь испытывать удачу каждые 24 часа! ⭐\n\n"
        "ОТКРЫВАЙ БЕСПЛАТНЫЙ КЕЙС КАЖДЫЕ 24 ЧАСА\n\n"
        "★ Подарок, TON или Stars — что выпадет сегодня?\n\n"
        "Открывай бесплатный кейс раз в 24 часа и проверяй удачу 🎁"
    )
    
    share_url = f"https://t.me/share/url?url={ref_link}&text={share_text}"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📤 ПОДЕЛИТЬСЯ", url=share_url)],
        [InlineKeyboardButton(text="📋 КОПИРОВАТЬ ССЫЛКУ", callback_data=f"copy_ref_{callback.from_user.id}")],
        [InlineKeyboardButton(text="« НАЗАД", callback_data="back_to_start")]
    ])
    
    await callback.message.edit_text(
        f"👥 <b>Реферальная система</b>\n\n"
        f"Приглашай друзей и получай бонусы:\n"
        f"• 1 друг = 2 ⭐\n"
        f"• 5 друзей = 10 ⭐ + бесплатный кейс\n"
        f"• 10 друзей = 20 ⭐ + 3 бесплатных кейса\n\n"
        f"<b>Твоя ссылка:</b>\n<code>{ref_link}</code>\n\n"
        f"Нажми «ПОДЕЛИТЬСЯ» чтобы отправить пост друзьям!",
        parse_mode="HTML",
        reply_markup=keyboard
    )
    
    await callback.answer()

@dp.callback_query(lambda c: c.data == "back_to_start")
async def back_to_start(callback: types.CallbackQuery):
    """Возврат в главное меню"""
    
    webapp_url = f"{WEBAPP_URL}?start={callback.from_user.id}"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎁 ОТКРЫТЬ БЕСПЛАТНЫЙ КЕЙС", web_app=WebAppInfo(url=webapp_url))],
        [InlineKeyboardButton(text="👥 ПРИГЛАСИТЬ ДРУЗЕЙ", callback_data="invite")],
        [
            InlineKeyboardButton(text="📋 Пользовательское соглашение", url="https://t.me/durov"),
            InlineKeyboardButton(text="💬 Поддержка", url="https://t.me/debashev")
        ],
        [InlineKeyboardButton(text="🌟 Присоединиться к сообществу", url=COMMUNITY_URL)]
    ])
    
    await callback.message.edit_text(
        f"🎁 <b>VILLD GIFT</b>\n"
        f"👥 17,812 пользователей\n\n"
        f"Реклама VILLD GIFT\n"
        f"Что это?\n"
        f"Ежедневный бесплатный кейс каждые 24 часа. Внутри случайный подарок 🎁\n\n"
        f"Try your luck in daily gift raffles at @VilldGiftBot\n"
        f"Open cases and win amazing prizes every day!",
        parse_mode="HTML",
        reply_markup=keyboard
    )
    
    await callback.answer()

@dp.callback_query(lambda c: c.data and c.data.startswith("copy_ref_"))
async def copy_ref_link(callback: types.CallbackQuery):
    """Копирование реферальной ссылки"""
    
    user_id = callback.data.split("_")[2]
    bot_info = await bot.me()
    ref_link = f"https://t.me/{bot_info.username}?start={user_id}"
    
    await callback.answer(f"📋 Ссылка скопирована!\n{ref_link}", show_alert=True)

async def main():
    """Запуск бота"""
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
