import asyncio
import logging
import json
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, LabeledPrice

# ========== НАСТРОЙКИ ==========
BOT_TOKEN = "8648458601:AAE-Rb0Y0ZAWuKJt3MZFwBzq0S9STRMBDSE"
WEBAPP_URL = "https://personawoodoo.github.io/WILLD-GIFT/"
CHANNEL_URL = "https://t.me/VILLD_GIFT"
SUPPORT_URL = "https://t.me/debashev"
PHOTO_URL = "https://i.supaimg.com/435c46f7-76b1-41ba-82e2-1f1a0a964f2c/bc2e341f-0e5f-4a83-80e6-d9801cc1025d.jpg"
ADMIN_ID = 8478884644

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ========== ОБРАБОТКА ДАННЫХ ИЗ МИНИ-ПРИЛОЖЕНИЯ ==========
@dp.message(F.web_app_data)
async def web_app_data_handler(message: types.Message):
    """Принимаем данные из мини-приложения"""
    try:
        data = json.loads(message.web_app_data.data)
        action = data.get('action')
        
        if action == 'buy_stars':
            amount = int(data.get('amount', 500))
            prices = [LabeledPrice(label="Пополнение баланса", amount=amount)]
            
            await message.answer_invoice(
                title="Пополнение VILLD GIFT",
                description=f"Пополнение баланса на {amount} звёзд",
                payload=f"stars_{amount}_{message.from_user.id}",
                provider_token="",
                currency="XTR",
                prices=prices,
                start_parameter="topup",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="💳 Оплатить звёздами", pay=True)],
                    [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_payment")]
                ])
            )
            
        elif action == 'share_ref':
            ref_code = data.get('ref_code', '')
            bot_info = await bot.me()
            ref_link = f"https://t.me/{bot_info.username}?start={ref_code}"
            share_text = "Открывай Free Box в VILLD GIFT и забирай свои NFT-подарки! 🎁\n\nЭто на 100% бесплатно, можешь испытывать удачу каждые 24 часа! ⭐\n\nVILLD GIFT\nБЕСПЛАТНЫЙ КЕЙС КАЖДЫЕ 24 ЧАСА!"
            share_url = f"https://t.me/share/url?url={ref_link}&text={share_text}"
            
            await message.answer_photo(
                photo=PHOTO_URL,
                caption=f"👥 Твоя реферальная ссылка:\n{ref_link}",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="📤 ПОДЕЛИТЬСЯ", url=share_url)]
                ])
            )
            
    except Exception as e:
        logging.error(f"Ошибка WebAppData: {e}")

@dp.callback_query(lambda c: c.data == "cancel_payment")
async def cancel_payment(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.answer("Оплата отменена")

@dp.pre_checkout_query()
async def process_pre_checkout(pre_checkout_query: types.PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)

@dp.message(F.successful_payment)
async def process_successful_payment(message: types.Message):
    payment = message.successful_payment
    amount = payment.total_amount
    
    await message.answer(
        f"✅ Оплата прошла успешно!\n"
        f"💰 На ваш баланс зачислено {amount} ⭐",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🎁 ОТКРЫТЬ МИНИ-ПРИЛОЖЕНИЕ", web_app=WebAppInfo(url=WEBAPP_URL))]
        ])
    )

# ========== КОМАНДА /START ==========
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    ref_code = message.text.split()[1] if len(message.text.split()) > 1 else None
    webapp_url = WEBAPP_URL
    if ref_code:
        webapp_url = f"{WEBAPP_URL}?start={ref_code}"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎁 ОТКРЫТЬ", web_app=WebAppInfo(url=webapp_url))],
        [InlineKeyboardButton(text="📢 КАНАЛ", url=CHANNEL_URL)],
        [InlineKeyboardButton(text="💬 ПОДДЕРЖКА", url=SUPPORT_URL)]
    ])
    
    await message.answer_photo(
        photo=PHOTO_URL,
        caption="🎁 БЕСПЛАТНОЕ ВРАЩЕНИЕ КАЖДЫЕ 24 ЧАСА!",
        reply_markup=keyboard
    )

# ========== КОМАНДА /INVITE ==========
@dp.message(Command("invite"))
async def cmd_invite(message: types.Message):
    bot_info = await bot.me()
    ref_link = f"https://t.me/{bot_info.username}?start={message.from_user.id}"
    share_text = "🎁 Try your luck in daily gift raffles at @VilldGiftBot\n✨ Open cases and win amazing prizes every day!"
    share_url = f"https://t.me/share/url?url={ref_link}&text={share_text}"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📤 ПОДЕЛИТЬСЯ", url=share_url)]
    ])
    
    await message.answer_photo(
        photo=PHOTO_URL,
        caption=f"👥 Твоя реферальная ссылка:\n{ref_link}",
        reply_markup=keyboard
    )

# ========== КОМАНДА /GIFT (ОТПРАВКА ПОДАРКА) ==========
@dp.message(Command("gift"))
async def cmd_gift(message: types.Message):
    args = message.text.split()
    if len(args) < 2:
        await message.answer("Использование: /gift @username")
        return
    
    recipient = args[1].replace("@", "")
    
    gift_text = (
        f"🎁 <b>Вам отправили подарок!</b>\n\n"
        f"Отправитель: @{message.from_user.username or 'Пользователь'}\n"
        f"Чтобы получить подарок, нажмите на кнопку ниже!"
    )
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎁 ЗАБРАТЬ ПОДАРОК", web_app=WebAppInfo(url=WEBAPP_URL))],
        [InlineKeyboardButton(text="📢 КАНАЛ", url=CHANNEL_URL)]
    ])
    
    try:
        await bot.send_photo(
            chat_id=f"@{recipient}",
            photo=PHOTO_URL,
            caption=gift_text,
            parse_mode="HTML",
            reply_markup=keyboard
        )
        await message.answer(f"✅ Подарок успешно отправлен @{recipient}!")
        await bot.send_message(chat_id=ADMIN_ID, text=f"📨 Подарок от @{message.from_user.username} для @{recipient}")
    except Exception as e:
        await message.answer(f"❌ Ошибка отправки: {e}")

# ========== КОМАНДА /HELP ==========
@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    help_text = (
        "🎁 <b>VILLD GIFT — Команды:</b>\n\n"
        "/start — Главное меню\n"
        "/invite — Реферальная ссылка\n"
        "/gift @username — Отправить подарок\n"
        "/help — Помощь"
    )
    await message.answer(help_text, parse_mode="HTML")

# ========== ЗАПУСК ==========
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
