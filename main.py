import logging
import os
import random
from flask import Flask
from threading import Thread
from telegram import Update, ChatPermissions
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- Keep Alive ---
app_flask = Flask('')
@app_flask.route('/')
def home(): return "မြနှင်း Bot Online ❤️"

def run():
    port = int(os.environ.get("PORT", 8080))
    app_flask.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- Settings & Data ---
TOKEN = os.environ.get("BOT_TOKEN") 
OWNER_ID = 7771663458  
registered_users = {} 
group_list = {}
game_db = {"mbb": [], "pubg": []} 

AD_TEXT = ("\n\n━━━━━━━━━━━━━━\n📢 https://t.me/+FFbLsHyYIAg4YmU1\nရည်းစားရှာဖွေရေး gp ကို join ပေးကျပါရှင့် 🥰😘✅")

logging.basicConfig(level=logging.INFO)

async def is_admin_or_owner(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    if update.effective_chat.type == "private": return False
    user_id = update.effective_user.id
    if user_id == OWNER_ID: return True
    try:
        member = await context.bot.get_chat_member(update.effective_chat.id, user_id)
        return member.status in ['administrator', 'creator']
    except: return False

# --- Functions ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type in ["group", "supergroup"]: group_list[update.effective_chat.id] = update.effective_chat.title
    start_msg = f"🎀 မင်္ဂလာပါရှင့် **မြနှင်း** ပါရှင့်။\n👑 Owner: @Tear808\n📖 အသုံးပြုပုံကြည့်ရန် - /help ကို နှိပ်ပေးပါရှင့်။{AD_TEXT}"
    await update.message.reply_text(start_msg, parse_mode='Markdown')

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_msg = (
        "✨ **မြနှင်း Bot အသုံးပြုနည်း** ✨\n\n"
        "👤 /boy , /girl - စာရင်းသွင်းရန်\n"
        "💖 /love - အတွဲချိတ်ရန်\n"
        "🎮 /mbbfriend , /pubgfriend - ဂိမ်းဖော်ရှာရန်\n"
        "📢 /admin - Admin ခေါ်ရန်\n"
        "👥 /allmember - Member အားလုံး @ ခေါ်ရန် (Admin)\n\n"
        "🛡 **Admin Tools**\n"
        "🚫 /ban , 🤫 /mute , 🔊 /umute\n🚀 /bcast (Owner)"
    )
    await update.message.reply_text(help_msg)

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id
    if not user.username: await update.message.reply_text("❌ Username အရင်ဆောက်ပေးပါဦးနော်။"); return
    gender = "Boy 👨" if "boy" in update.message.text.lower() else "Girl 👩"
    if chat_id not in registered_users: registered_users[chat_id] = {}
    registered_users[chat_id][user.id] = {"username": f"@{user.username}", "gender": gender}
    await update.message.reply_text(f"✨ {gender} အဖြစ် မှတ်တမ်းတင်လိုက်ပြီနော်! 🥰")

async def love_match(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    if chat_id not in registered_users or user_id not in registered_users[chat_id]:
        await update.message.reply_text("🚨 အရင်ဆုံး /boy ဒါမှမဟုတ် /girl နဲ့ စာရင်းသွင်းပါဦး သဲလေးရဲ့... 🥺💗")
        return
    me = registered_users[chat_id][user_id]
    potential = [uid for uid, data in registered_users[chat_id].items() if uid != user_id and data["gender"] != me["gender"]]
    if not potential: await update.message.reply_text("⏳ ဖူးစာရှင်လေးတွေ ရှာမတွေ့သေးဘူးရှင့်... 🥺💕"); return
    partner = registered_users[chat_id][random.choice(potential)]
    await update.message.reply_text(f"💘 **မြှားနတ်မောင် မြှားပစ်လိုက်ပြီရှင့်** 🏹\n❤️ {me['username']} ❤️ {partner['username']}\nမြန်မြန်လေး ညားကြပါစေရှင့်! 🥰", parse_mode='Markdown')

async def game_friend(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    g_type = "mbb" if "mbb" in update.message.text.lower() else "pubg"
    if game_db[g_type]:
        partner_id, partner_name = game_db[g_type].pop()
        await update.message.reply_text(f"🎮 **ဂိမ်းဖော် တွေ့ပြီရှင့်!**\n@{user.username} နဲ့ @{partner_name} တို့ရေ... အတူတူ ဆော့လို့ရပြီနော်! 🎀✨")
    else:
        game_db[g_type].append((user.id, user.username))
        await update.message.reply_text(f"⏳ @{user.username} ရေ... {g_type.upper()} အဖော် ရှာပေးနေတယ်နော်... စောင့်ပေးပါဦးရှင့်! 🥺🙏")

async def admin_tools(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin_or_owner(update, context) or not update.message.reply_to_message: return
    target = update.message.reply_to_message.from_user
    cmd = update.message.text.lower()
    if '/ban' in cmd:
        await context.bot.ban_chat_member(update.effective_chat.id, target.id)
        await update.message.reply_text(f"🚨 @{target.username} ကို ထွက်သွားခိုင်းလိုက်ပါပြီ! 🤬")
    elif '/mute' in cmd:
        await context.bot.restrict_chat_member(update.effective_chat.id, target.id, ChatPermissions(can_send_messages=False))
        await update.message.reply_text(f"🤫 @{target.username} ရေ... ခဏလေး အသံတိတ်ပေးပါဦးနော်! 🤐")
    elif '/umute' in cmd:
        await context.bot.restrict_chat_member(update.effective_chat.id, target.id, ChatPermissions(can_send_messages=True))
        await update.message.reply_text(f"🔊 @{target.username} ကို ပြန်ချစ်ပေးလိုက်ပါပြီနော်! 😘")

# --- Main ---
def main():
    if not TOKEN: return
    keep_alive()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler(["boy", "girl"], register))
    app.add_handler(CommandHandler("love", love_match))
    app.add_handler(CommandHandler(["mbbfriend", "pubgfriend"], game_friend))
    app.add_handler(CommandHandler(["ban", "mute", "umute"], admin_tools))
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, lambda u, c: group_list.update({u.effective_chat.id: u.effective_chat.title})))
    app.run_polling()

if __name__ == '__main__': main()
