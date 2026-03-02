from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ContextTypes
from config.config import WEBHOOK_URL, WEBAPP_PATH
from db.users_crud import create_user, get_user_by_telegram_id, update_user_username
from logs.logger import logger

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = await get_user_by_telegram_id(update.effective_chat.id)
    if not user:
        user = await create_user(update.effective_chat.id, update.effective_user.username)
    logger.info(f"Пользователь {user.id} ({user.username}) ({user.telegram_id}) ({user.created_at}) начал диалог")
    #await update_user_email(update.effective_chat.id, 'test@test.com')
    # user = await update_user_username(user.telegram_id, update.effective_user.username)
    # logger.info(f"Пользователь {user.id} ({user.username}) ({user.telegram_id}) ({user.created_at}) обновлен")
    keyboard = [
        [InlineKeyboardButton("✅ Вступить в клуб", callback_data="menu_join")],
        [InlineKeyboardButton("ℹ️ Зачем тебе в клуб", callback_data="menu_why")],
        [InlineKeyboardButton("🧑‍💻 Поддержка", url="https://t.me/alexnpmfk")],
        [InlineKeyboardButton("⭐ Отзывы", url="https://t.me/sau_bot_reviews")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Привет, я ваш помощник bot_sau.",
        reply_markup=reply_markup,
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "menu_join":
        payment_keyboard = [
            [InlineKeyboardButton("💳 Оплатить картой РФ",web_app=WebAppInfo(url=WEBHOOK_URL + WEBAPP_PATH))],
            [
                InlineKeyboardButton(
                    "🌍 Оплатить зарубежной картой", web_app=WebAppInfo(url=WEBHOOK_URL + WEBAPP_PATH))
                
            ],
            [InlineKeyboardButton("↩️ Назад", callback_data="back_to_menu")],
        ]
        payment_markup = InlineKeyboardMarkup(payment_keyboard)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Выберите способ оплаты",
            reply_markup=payment_markup,
        )
    elif query.data == "pay_rf":
        await query.message.reply_text("Оплата картой РФ: (ссылку)")

    elif query.data == "pay_foreign":
        await query.message.reply_text("Оплата зарубежной картой: (ссылку)")

    elif query.data == "back_to_menu":
        await start(update, context)

    elif query.data == "menu_why":
        await query.message.reply_text(
            "Почему стоит вступить?\n\n• Поддержка\n• Материалы\n• Комьюнити\n"
        )
