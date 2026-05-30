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

AD_TEXT = f"\n\n━━━━━━━━━━━━━━\n📢 https://t.me/Truelove150080\nရည်းစားရှာဖွေရေး gp ကို join ပေးကျပါရှင့် 🥰😘✅"

logging.basicConfig(level=logging.INFO)

def is_owner(user_id): return user_id == OWNER_ID

# --- ✨ လူသစ်ဝင်လာခြင်း ---
async def welcome_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.new_chat_members: return
    chat = update.effective_chat
    group_list[chat.id] = chat.title
    for member in update.message.new_chat_members:
        if member.id == context.bot.id: continue
        username = f"@{member.username}" if member.username else f"[{member.first_name}](tg://user?id={member.id})"
        welcome_msg = (
            f"ဟယ်... အချောလေး {username} ရေ... 😍✨\n"
            f"ငါတို့ GP ထဲ ရောက်လာပြီဟယ်... ချောလိုက်တာနော် လူလေးရာ။ 🥰💋\n\n"
            f"🎀 **မြနှင်း** ရဲ့ နွေးထွေးတဲ့ ရင်ခွင်ထဲကို ကြိုဆိုပါတယ်ရှင့်။"
        )
        await update.message.reply_text(welcome_msg, parse_mode='Markdown')

# --- 💖 မြှားနတ်မောင် (ဆုတောင်းစကားအပြည့်အစုံ) ---
async def love_match(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    if chat_id not in registered_users or user_id not in registered_users[chat_id]:
        await update.message.reply_text("🚨 အရင်ဆုံး /boy ဒါမှမဟုတ် /girl နဲ့ စာရင်းသွင်းပါဦး သဲလေး။")
        return
    me = registered_users[chat_id][user_id]
    potential = [uid for uid, data in registered_users[chat_id].items() if uid != user_id and data["gender"] != me["gender"]]
    if not potential:
        await update.message.reply_text("⏳ ဖူးစာရှင်လေးတွေ ရှာမတွေ့သေးဘူးရှင့်... 🥺💕")
        return
    partner = registered_users[chat_id][random.choice(potential)]
    match_msg = (
        f"💘 **မြှားနတ်မောင် မြှားပစ်လိုက်ပြီရှင့်** 🏹🎯✨\n\n"
        f"🌹 **အတွဲလေးကတော့** 🌹\n"
        f"❤️ {me['username']} ❌ ❤️ {partner['username']}\n\n"
        f"မြန်မြန်လေး ညားကြပါစေရှင့်! 🥰\n"
        f"**နောင်တစ်သက်လုံးလည်း အချစ်တွေ တိုးပွားပါစေရှင့်!** 🤪🔥💕💋✨"
    )
    await update.message.reply_text(match_msg, parse_mode='Markdown')

# --- 🛡 အရေးပေါ်စနစ် (Ban/Mute/Unmute) ---
async def admin_tools(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id): return
    if not update.message.reply_to_message: return
    target = update.message.reply_to_message.from_user
    cmd = update.message.text.lower()
    try:
        if '/ban' in cmd:
            await context.bot.ban_chat_member(update.effective_chat.id, target.id)
            await update.message.reply_text(f"🚨 **အရေးပေါ်စနစ်ဖြင့် နှင်ထုတ်ခြင်း** 🚨\n\n@{target.username} ကို GP ထဲကနေ အပြီးအပိုင် မောင်းထုတ်လိုက်ပါပြီ! 🤬💢🔥")
        elif '/mute' in cmd:
            await context.bot.restrict_chat_member(update.effective_chat.id, target.id, ChatPermissions(can_send_messages=False))
            await update.message.reply_text(f"🤫 **အရေးပေါ်စနစ်ဖြင့် မြူခြင်း** 🤫\n\n@{target.username} စကားများလွန်းလို့ နှုတ်ခမ်းလေးကို ခေတ္တပိတ်ထားလိုက်ပြီနော်! 🤐🔇🚫")
        elif '/umute' in cmd:
            await context.bot.restrict_chat_member(update.effective_chat.id, target.id, ChatPermissions(can_send_messages=True))
            await update.message.reply_text(f"🔊 **အရေးပေါ်စနစ်ဖြင့် မြူဖြုတ်ခြင်း** 🔊\n\n@{target.username} လိမ်မာသွားပြီထင်လို့ စကားပြန်ပြောခွင့်ပေးလိုက်ပါပြီရှင့်! 😘✅✨")
    except Exception as e: logging.error(f"Admin Error: {e}")

# --- 🚀 Broadcast (Detailed Report) ---
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id) or not update.message.reply_to_message: return
    target_msg = update.message.reply_to_message
    success, fail, report = 0, 0, "📊 **Detailed Broadcast Report**\n\n"
    for chat_id, title in list(group_list.items()):
        try:
            await context.bot.copy_message(chat_id=chat_id, from_chat_id=update.effective_chat.id, message_id=target_msg.message_id)
            report += f"✅ {title or chat_id}\n"; success += 1
        except:
            report += f"❌ {title or chat_id}\n"; fail += 1; group_list.pop(chat_id, None)
    await update.message.reply_text(f"{report}\n🎯 စုစုပေါင်း: {success+fail} | အောင်မြင်: {success} | ရှုံး: {fail}", parse_mode='Markdown')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type in ["group", "supergroup"]: group_list[update.effective_chat.id] = update.effective_chat.title
    await update.message.reply_text(f"✨ **မြနှင်း Bot လမ်းညွှန်** ✨\n\n👤 /boy , /girl - စာရင်းသွင်း\n💖 /love - အတွဲချိတ်{AD_TEXT}", parse_mode='Markdown')

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not user.username: await update.message.reply_text("❌ Username အရင်ဆောက်ပေးပါဦးနော်။"); return
    gender = "Boy 👨" if "boy" in update.message.text.lower() else "Girl 👩"
    if update.effective_chat.id not in registered_users: registered_users[update.effective_chat.id] = {}
    registered_users[update.effective_chat.id][user.id] = {"username": f"@{user.username}", "gender": gender}
    await update.message.reply_text(f"✨ {gender} အဖြစ် မှတ်တမ်းတင်လိုက်ပြီနော်! 🥰")

def main():
    if not TOKEN: return
    keep_alive()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_member))
    app.add_handler(CommandHandler(["start", "help"], start))
    app.add_handler(CommandHandler("bcast", broadcast))
    app.add_handler(CommandHandler(["boy", "girl"], register))
    app.add_handler(CommandHandler("love", love_match))
    app.add_handler(CommandHandler(["ban", "mute", "umute"], admin_tools))
    app.add_handler(MessageHandler(filters.ChatType.GROUPS & ~filters.COMMAND, lambda u, c: group_list.update({u.effective_chat.id: u.effective_chat.title})))
    app.run_polling()

if __name__ == '__main__': main()
  
