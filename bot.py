from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, LabeledPrice
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes, PreCheckoutQueryHandler
import json, logging

TOKEN = "8648458601:AAE-Rb0Y0ZAWuKJt3MZFwBzq0S9STRMBDSE"
MINI_APP_URL = "https://personawoodoo.github.io/WILLD-GIFT/index.html"
CHANNEL_LINK = "https://t.me/VILLD_GIFT"
START_PHOTO = "https://i.supaimg.com/435c46f7-76b1-41ba-82e2-1f1a0a964f2c/494659da-9570-4253-8576-31ccbe9a3905.jpg"

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # ... стандартное приветствие с фото и кнопкой ИГРАТЬ ...
    pass

async def web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка данных из мини‑приложения (покупка звёзд)"""
    data = json.loads(update.effective_message.web_app_data.data)
    if data.get('action') == 'buy_stars':
        amount = data['amount']
        title = f"Пополнение {amount} ⭐"
        description = f"Пополнение баланса на {amount} звёзд в VILLD GIFT"
        payload = f"stars_{amount}"
        currency = "XTR"
        prices = [LabeledPrice(title, amount * 100)]  # Цена в минимальных единицах
        await context.bot.send_invoice(
            chat_id=update.effective_chat.id,
            title=title,
            description=description,
            payload=payload,
            provider_token="",  # Для звёзд не нужен токен
            currency=currency,
            prices=prices,
            start_parameter="buy_stars"
        )
        await update.effective_message.reply_text("Счёт отправлен. После оплаты перезайдите в мини-приложение.")

async def successful_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Подтверждение оплаты""" 
    await update.effective_message.reply_text("✅ Оплата прошла! Теперь ваш баланс пополнен. Зайдите в мини-приложение.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_data))
    app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment))
    app.run_polling()
