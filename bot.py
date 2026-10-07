import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# ដាក់ Token របស់ Bot អ្នកនៅទីនេះ ឬក្នុង Environment Variables របស់ Railway
BOT_TOKEN = os.getenv("BOT_TOKEN", "ដាក់_TOKEN_របស់អ្នក_ទីនេះ")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = f"@{user.username}" if user.username else user.first_name
    
    welcome_text = f"សួស្ដី {username} ស្វាគមន៍មកកាន់ MT5 SMM PANEL!"
    
    # ប៊ូតុងប្ដូរភាសា (Inline Buttons)
    lang_keyboard = [
        [
            InlineKeyboardButton("🇰🇭 ខ្មែរ", callback_data="lang_kh"),
            InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(lang_keyboard)
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    # ពេលជ្រើសរើសភាសារួច បង្ហាញ Menu គោល
    if query.data in ["lang_kh", "lang_en"]:
        menu_keyboard = [
            [KeyboardButton("👨🏻‍💻 គណនី"), KeyboardButton("🛍️ ហាងសេវា Facebook")],
            [KeyboardButton("💰 ដាក់ប្រាក់"), KeyboardButton("📖 របៀបប្រើប្រាស់")],
            [KeyboardButton("🛒 បញ្ជីទិញរបស់អ្នក")]
        ]
        reply_markup = ReplyKeyboardMarkup(menu_keyboard, resize_keyboard=True)
        
        text = "សូមជ្រើសរើសសេវាកម្មខាងក្រោម៖" if query.data == "lang_kh" else "Please choose a service below:"
        await query.message.reply_text(text, reply_markup=reply_markup)

async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.effective_user
    
    if text == "👨🏻‍💻 គណនី":
        username = f"@{user.username}" if user.username else "គ្មាន"
        account_info = (
            "👤 <b>ព័ត៌មានគណនីរបស់អ្នក</b>\n"
            "━━━━━━━━━━━━━━━\n"
            f"🔹 <b>Username:</b> {username}\n"
            f"🔹 <b>ID:</b> <code>{user.id}</code>\n"
            f"🔹 <b>Balance:</b> $0.00\n"
            f"🔹 <b>Rank:</b> ធម្មតា (Member)\n"
            "━━━━━━━━━━━━━━━"
        )
        await update.message.reply_html(account_info)
        
    elif text == "🛍️ ហាងសេវា Facebook":
        await update.message.reply_text("បញ្ជីសេវាកម្ម Facebook ៖\n- បង្កើន Like\n- បង្កើន Follow\n- បង្កើន View")
        
    elif text == "💰 ដាក់ប្រាក់":
        await update.message.reply_text("💳 សូមទាក់ទង Admin ដើម្បីដាក់ប្រាក់ ឬផ្ញើវិក័យប័ត្រទីនេះ។")
        
    elif text == "📖 របៀបប្រើប្រាស់":
        await update.message.reply_text("សេចក្ដីណែនាំ៖\n១. ជ្រើសរើសសេវាកម្ម\n២. ដាក់ Link\n៣. បញ្ចូលចំនួន\n៤. រង់ចាំលទ្ធផល")
        
    elif text == "🛒 បញ្ជីទិញរបស់អ្នក":
        await update.message.reply_text("ប្រវត្តិការបញ្ជាទិញរបស់អ្នកទទេស្អាត។")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_messages))
    
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
