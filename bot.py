#!/usr/bin/env python3
import json
import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, LabeledPrice
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    PreCheckoutQueryHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

# ---------- НАСТРОЙКИ ----------
TOKEN = "8648458601:AAE-Rb0Y0ZAWuKJt3MZFwBzq0S9STRMBDSE"
MINI_APP_URL = "https://personawoodoo.github.io/WILLD-GIFT/index.html"
CHANNEL_LINK = "https://t.me/VILLD_GIFT"
START_PHOTO = "https://i.supaimg.com/435c46f7-76b1-41ba-82e2-1f1a0a964f2c/494659da-9570-4253-8576-31ccbe9a3905.jpg"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------- КОМАНДЫ ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Приветственное сообщение с фото и кнопкой «ИГРАТЬ»."""
    caption = (
        "🎁 <b>VILLD GIFT</b>\n\n"
        "<b>БЕСПЛАТНОЕ ОТКРЫТИЕ</b>\n"
        "<b>КАЖДЫЕ 24 ЧАСА!</b>\n\n"
        "🕐 <b>1 РАЗ В 24 ЧАСА</b>\n"
        "💎 <b>ЦЕННЫЕ ПРИЗЫ</b>\n"
        "✅ <b>ЧЕСТНО И ПРОЗРАЧНО</b>\n\n"
        f"<b>📢 Канал:</b> {CHANNEL_LINK}"
    )

    keyboard = [
        [InlineKeyboardButton("🎰 ИГРАТЬ", web_app={"url": MINI_APP_URL})],
        [
            InlineKeyboardButton("📢 Канал", url=CHANNEL_LINK),
            InlineKeyboardButton("👥 Пригласить друга", switch_inline_query="Приглашаю в VILLD GIFT!"),
        ],
        [InlineKeyboardButton("ℹ️ О проекте", callback_data="about")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        await update.message.reply_photo(
            photo=START_PHOTO,
            caption=caption,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML,
        )
    except Exception as e:
        logger.error(f"Ошибка отправки фото: {e}")
        await update.message.reply_text(
            text=caption,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML,
        )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает нажатия на inline‑кнопки."""
    query = update.callback_query
    await query.answer()

    if query.data == "about":
        text = (
            "🎁 <b>VILLD GIFT v2.0</b>\n\n"
            "Первое мини‑приложение для открытия кейсов с NFT‑подарками Telegram.\n\n"
            "▫️ Кейсы с разной стоимостью\n"
            "▫️ Мульти‑открытие до 10 кейсов\n"
            "▫️ Бесплатный кейс раз в 24 часа\n"
            "▫️ Инвентарь с выводом подарков\n"
            "▫️ Реферальная система\n"
            "▫️ Пополнение через Stars и TON\n\n"
            "Разработчик: @debashev"
        )
        await query.message.reply_text(text, parse_mode=ParseMode.HTML)

# ---------- ОБРАБОТКА ДАННЫХ ИЗ МИНИ‑ПРИЛОЖЕНИЯ ----------
async def web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Принимает данные из мини‑приложения (покупка звёзд)."""
    try:
        data = json.loads(update.effective_message.web_app_data.data)
    except (json.JSONDecodeError, AttributeError):
        await update.effective_message.reply_text("❌ Неверный формат данных.")
        return

    if data.get("action") == "buy_stars":
        amount = data["amount"]
        title = f"Пополнение {amount} ⭐"
        description = f"Покупка {amount} звёзд для VILLD GIFT"
        payload = f"stars_{amount}"
        currency = "XTR"
        prices = [LabeledPrice(title, amount * 100)]  # Цена в минимальных единицах (1 звёзда = 100)

        await context.bot.send_invoice(
            chat_id=update.effective_chat.id,
            title=title,
            description=description,
            payload=payload,
            provider_token="",   # для звёзд не нужен
            currency=currency,
            prices=prices,
            start_parameter="buy_stars",
        )
    else:
        await update.effective_message.reply_text("✅ Данные получены, но действие не распознано.")

# ---------- ПЛАТЕЖИ ----------
async def pre_checkout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Подтверждение перед оплатой."""
    await update.pre_checkout_query.answer(ok=True)

async def successful_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Успешная оплата – уведомление."""
    await update.message.reply_text(
        "✅ Оплата прошла! Ваш баланс пополнен. Зайдите в мини‑приложение, чтобы увидеть изменения."
    )

# ---------- ЗАПУСК ----------
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_data))
    app.add_handler(PreCheckoutQueryHandler(pre_checkout))
    app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment))

    logger.info("Бот VILLD GIFT запущен")
    app.run_polling()

if __name__ == "__main__":
    main()
