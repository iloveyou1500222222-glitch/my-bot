import os
import random
import logging
from telegram import Update, ChatPermissions
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.error import TelegramError

# ၁။ လုံခြုံရေးအတွက် Token
TOKEN = "8630120862:AAE-dAcieQOQMcKfjKgKLHdtEOi9nTtidyY" 
OWNER_ID = 7771663458  

# In-Memory Database
users_db = {} 
waiting_boys = set()
waiting_girls = set()
AD_TEXT = "\n\n📢 ကြော်ငြာထည့်ရန် @Tear808 သို့သွားထည့်ပေးပါရှင့်💝✅"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def check_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    if update.effective_chat.type == "private": return False
    user_id = update.effective_user.id
    if user_id == OWNER_ID: return True
    member = await context.bot.get_chat_member(update.effective_chat.id, user_id)
    return member.status in ['administrator', 'creator']

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"မင်္ဂလာပါရှင့်။" + AD_TEXT)

async def set_gender(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.username or "No Username"
    cmd = update.message.text.lower()
    if "boy" in cmd:
        users_db[user_id] = {"gender": "boy", "username": username}
        waiting_girls.discard(user_id)
        waiting_boys.add(user_id)
        await update.message.reply_text("👦 မှတ်ပုံတင်ပြီးပါပြီ။ /love နဲ့ အတွဲရှာနိုင်ပါပြီ။")
    elif "girl" in cmd:
        users_db[user_id] = {"gender": "girl", "username": username}
        waiting_boys.discard(user_id)
        waiting_girls.add(user_id)
        await update.message.reply_text("👧 မှတ်ပုံတင်ပြီးပါပြီ။ /love နဲ့ အတွဲရှာနိုင်ပါပြီ။")

async def match_love(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in users_db:
        await update.message.reply_text("❌ အရင်ဆုံး /boy (သို့) /girl ဟု ရိုက်ပေးပါ။")
        return
    user_gender = users_db[user_id]["gender"]
    target_pool = waiting_girls if user_gender == "boy" else waiting_boys
    if not target_pool:
        await update.message.reply_text("⏳ ဖူးစာဖက် မရှိသေးလို့ ခဏစောင့်ပေးပါနော်...")
        return
    partner_id = random.choice(list(target_pool))
    target_pool.remove(partner_id)
    partner_info = users_db[partner_id]
    username = f"@{partner_info['username']}" if partner_info['username'] != "No Username" else f"ID: {partner_id}"
    await update.message.reply_text(f"🎉 အတွဲချိတ်မိသွားပါပြီရှင်! ဖူးစာဖက်ကတော့ 👉 {username} ဖြစ်ပါတယ်ရှင့်။ {AD_TEXT}")

async def ban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_admin(update, context): return
    if update.message.reply_to_message:
        target = update.message.reply_to_message.from_user
        try:
            await context.bot.ban_chat_member(update.effective_chat.id, target.id)
            await update.message.reply_text(f"🛑 {target.first_name} ကို မောင်းထုတ်လိုက်ပြီ။")
        except TelegramError as e: await update.message.reply_text(f"❌ အမှား - {e}")

async def mute_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_admin(update, context): return
    if update.message.reply_to_message:
        target = update.message.reply_to_message.from_user
        await context.bot.restrict_chat_member(update.effective_chat.id, target.id, permissions=ChatPermissions(can_send_messages=False))
        await update.message.reply_text(f"🔇 {target.first_name} ကို မြူလိုက်ပြီနော်...")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler(["boy", "girl"], set_gender))
    app.add_handler(CommandHandler("love", match_love))
    app.add_handler(CommandHandler("ban", ban_user))
    app.add_handler(CommandHandler("mute", mute_user))
    app.run_polling()

if __name__ == '__main__':
    main()
