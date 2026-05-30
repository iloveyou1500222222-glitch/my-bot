import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# Render ရဲ့ Environment Variables ထဲက Token ကို ယူပါမယ်
TOKEN = os.environ.get("BOT_TOKEN")

async def get_file_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.video:
        # ဗီဒီယိုပို့လိုက်ရင် ID ကို ပြန်ပြပေးမယ့်အပိုင်း
        file_id = update.message.video.file_id
        await update.message.reply_text(f"✅ Video File ID ရပါပြီ သဲလေး -\n\n`{file_id}`\n\nဒီ ID ကို Copy ကူးပြီး ကျွန်တော့်ကို ပြန်ပေးနော်။")

def main():
    if not TOKEN:
        print("Error: BOT_TOKEN not found!")
        return
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.VIDEO, get_file_id))
    print("Bot is running to get File ID...")
    app.run_polling()

if __name__ == '__main__':
    main()
  
