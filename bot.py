#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VILLD GIFT - Telegram Bot
Токен: 8648458601:AAE-Rb0Y0ZAWuKJt3MZFwBzq0S9STRMBDSE
Канал: @VILLD_GIFT
Мини-приложение: https://personawoodoo.github.io/WILLD-GIFT/
"""

import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Настройка
TOKEN = "8648458601:AAE-Rb0Y0ZAWuKJt3MZFwBzq0S9STRMBDSE"
MINI_APP_URL = "https://personawoodoo.github.io/WILLD-GIFT/index.html"
CHANNEL_USERNAME = "VILLD_GIFT"
CHANNEL_LINK = f"https://t.me/{CHANNEL_USERNAME}"

# Фото для стартового сообщения
START_PHOTO_URL = "https://i.supaimg.com/435c46f7-76b1-41ba-82e2-1f1a0a964f2c/494659da-9570-4253-8576-31ccbe9a3905.jpg"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Главное приветствие с фото"""
    
    caption = (
        f"🎁 <b>VILLD GIFT</b>\n\n"
        f"<b>БЕСПЛАТНОЕ ОТКРЫТИЕ</b>\n"
        f"<b>КАЖДЫЕ 24 ЧАСА!</b>\n\n"
        f"🕐 <b>1 РАЗ В 24 ЧАСА</b>\n"
        f"💎 <b>ЦЕННЫЕ ПРИЗЫ</b>\n"
        f"✅ <b>ЧЕСТНО И ПРОЗРАЧНО</b>\n\n"
        f"Открывай кейсы, собирай NFT-подарки, выигрывай!\n\n"
        f"<b>📢 Канал:</b> {CHANNEL_LINK}"
    )
    
    keyboard = [
        [InlineKeyboardButton("🎰 ИГРАТЬ", web_app={"url": MINI_APP_URL})],
        [
            InlineKeyboardButton("📢 Канал", url=CHANNEL_LINK),
            InlineKeyboardButton("👥 Пригласить друга", switch_inline_query="Приглашаю в VILLD GIFT!")
        ],
        [InlineKeyboardButton("ℹ️ О проекте", callback_data="about")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    try:
        await update.message.reply_photo(
            photo=START_PHOTO_URL,
            caption=caption,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
    except Exception as e:
        logger.error(f"Ошибка отправки фото: {e}")
        await update.message.reply_text(
            text=caption,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка нажатий на кнопки"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "about":
        about_text = (
            "🎁 <b>VILLD GIFT v2.0</b>\n\n"
            "Первое мини-приложение для открытия кейсов с NFT-подарками Telegram.\n\n"
            "<b>Возможности:</b>\n"
            "▫️ Кейсы с разной стоимостью\n"
            "▫️ Мульти-открытие до 10 кейсов\n"
            "▫️ Бесплатный кейс раз в 24 часа\n"
            "▫️ Инвентарь с выводом подарков\n"
            "▫️ Реферальная система\n"
            "▫️ Пополнение через Stars и TON\n\n"
            "Разработчик: @debashev"
        )
        await query.message.reply_text(about_text, parse_mode=ParseMode.HTML)

def main():
    """Запуск бота"""
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    print("🤖 Бот VILLD GIFT запущен!")
    print(f"📢 Канал: {CHANNEL_LINK}")
    print(f"🕹️ Мини-приложение: {MINI_APP_URL}")
    
    app.run_polling()

if __name__ == "__main__":
    main()
