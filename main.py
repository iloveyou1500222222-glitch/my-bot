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
def home(): return "မြနှင်း Bot Online & Secure ❤️"

def run():
    port = int(os.environ.get("PORT", 8080))
    app_flask.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- Settings & Data ---
TOKEN = os.environ.get("BOT_TOKEN") 
OWNER_ID = 7771663458  # သဲလေး ID
registered_users = {} 
group_list = set()  

WELCOME_VIDEO = "BAACAgUAAyEFAAT_ty-mAAIDemobPZxd25kTa7SNIjOF5_VhTZj7AAJuIAACyYXZVIh1A0X50n57OwQ" 

# ✅ ကြော်ငြာစာသား (/start မှာပဲ ပြပါမယ်)
BASE_LINK = "📢 https://t.me/Truelove150080"
CUSTOM_TEXT = "ရည်းစားရှာဖွေရေး gp ကို join ပေးကျပါရှင့် 🥰😘✅"
AD_TEXT = f"\n\n━━━━━━━━━━━━━━\n{BASE_LINK}\n{CUSTOM_TEXT}"

logging.basicConfig(level=logging.INFO)

# --- 🔐 Security: Admin & Owner Check ---
async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    if update.effective_chat.type == "private": return False
    user_id = update.effective_user.id
    if user_id == OWNER_ID: return True
    try:
        member = await context.bot.get_chat_member(update.effective_chat.id, user_id)
        return member.status in ['administrator', 'creator']
    except: return False

# --- ✨ ကြိုဆိုခြင်း (High Security & @ Mention) ---
async def welcome_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.new_chat_members: return
    for member in update.message.new_chat_members:
        if member.id == context.bot.id:
            group_list.add(update.effective_chat.id)
            continue
            
        username = f"@{member.username}" if member.username else f"[{member.first_name}](tg://user?id={member.id})"
        welcome_msg = (
            f"ဟယ်... အချောလေး {username} ရေ... 😍✨\n"
            f"ငါတို့ GP ထဲ ရောက်လာပြီဟယ်... ချောလိုက်တာနော် လူလေးရာ။ 🥰💋\n\n"
            f"သဲလေးရေ... လာ... **အခန်းထဲလာ**... 🍓💄\n"
            f"🎀 **မြနှင်း** ရဲ့ နွေးထွေးတဲ့ ရင်ခွင်ထဲကို ကြိုဆိုပါတယ်ရှင့်။"
        )
        try:
            await context.bot.send_video(chat_id=update.effective_chat.id, video=WELCOME_VIDEO, caption=welcome_msg, parse_mode='Markdown')
        except:
            await update.message.reply_text(welcome_msg, parse_mode='Markdown')

# --- 💖 Love Match (ချွဲနွဲ့ + လုံခြုံမှုရှိသော) ---
async def love_match(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    if chat_id not in registered_users or user_id not in registered_users[chat_id]:
        await update.message.reply_text("🚨 အရင်ဆုံး /boy ဒါမှမဟုတ် /girl နဲ့ စာရင်းသွင်းပါဦး အချောလေးရဲ့... 🥺💗")
        return
        
    me = registered_users[chat_id][user_id]
    potential = [uid for uid, data in registered_users[chat_id].items() if uid != user_id and data["gender"] != me["gender"]]
    
    if not potential:
        await update.message.reply_text("⏳ ဖူးစာရှင်လေးတွေ ရှာမတွေ့သေးဘူးရှင့်... ခဏစောင့်နော် အသည်းလေးတို့ 🥺💕")
        return
        
    partner = registered_users[chat_id][random.choice(potential)]
    match_msg = (
        f"💘 **မြှားနတ်မောင် မြှားပစ်လိုက်ပြီရှင့်** 🏹🎯✨\n\n"
        f"🌹 **တစ်သက်လုံး အချစ်တွေ တိုးပွားမယ့် အတွဲလေးကတော့** 🌹\n"
        f"┏━━━━━━━━━━━━━┓\n"
        f"   ❤️ {me['username']} \n"
        f"         ❌ \n"
        f"   ❤️ {partner['username']} \n"
        f"┗━━━━━━━━━━━━━┛\n\n"
        f"မြန်မြန်လေး ညားကြပါစေရှင့်... နောက်မှာလည်း တစ်သက်လုံး အချစ်တွေ တိုးပွားပါစေရှင့်! 🤪🔥💕💋"
    )
    await update.message.reply_text(match_msg, parse_mode='Markdown')

# --- 🛡 Admin Tools (ပိုမိုကောင်းမွန်သော လုံခြုံရေး) ---
async def admin_tools(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context): return # Admin မဟုတ်ရင် ဘာမှလုပ်မရ
    if not update.message.reply_to_message: return
    
    target = update.message.reply_to_message.from_user
    if target.id == OWNER_ID or target.id == context.bot.id: return # Owner နဲ့ Bot ကို Ban လို့မရအောင် ကာကွယ်ထားသည်
    
    cmd = update.message.text.lower()
    try:
        if '/ban' in cmd:
            await context.bot.ban_chat_member(update.effective_chat.id, target.id)
            await update.message.reply_text(f"📣 သွား... နင်ငါ့မျက်စိရှေ့က ပျောက်သွားတော့! 🤬 @{target.username} ကို နှင်ထုတ်လိုက်ပြီ! 😤")
        elif '/mute' in cmd:
            await context.bot.restrict_chat_member(update.effective_chat.id, target.id, ChatPermissions(can_send_messages=False))
            await update.message.reply_text(f"📣 စကားတွေ များနေလို့ ခဏမြူလိုက်ပြီနော်... 😘 @{target.username} လိမ်လိမ်မာမာနေဦး... 💋")
        elif '/umute' in cmd:
            await context.bot.restrict_chat_member(update.effective_chat.id, target.id, ChatPermissions(can_send_messages=True))
            await update.message.reply_text(f"📣 ကဲ... စကားပြန်ပြောလို့ ရပြီနော် သဲလေးရေ... 😘 @{target.username} ရယ်... အာဘွား! 💋✨")
    except: pass

# --- 🚀 Broadcast (Owner Only) ---
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID: return
    if not update.message.reply_to_message: return
    
    target_msg = update.message.reply_to_message
    for chat_id in list(group_list):
        try: await context.bot.copy_message(chat_id=chat_id, from_chat_id=update.effective_chat.id, message_id=target_msg.message_id)
        except: group_list.discard(chat_id)
    await update.message.reply_text("✅ ပို့စ်ဖြန့်ဝေပြီးပါပြီရှင့်။")

# --- အခြေခံ Commands ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type in ["group", "supergroup"]: group_list.add(update.effective_chat.id)
    await update.message.reply_text(f"မဂ်လာပါရှင့် 😘\n🎀**မြနှင်း**🎀 Bot လေး အဆင်သင့်ရှိပါတယ်ရှင့်။{AD_TEXT}", parse_mode='Markdown')

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id
    if not user.username:
        await update.message.reply_text("❌ Username အရင်ဆောက်ပေးပါဦးနော် အချောလေး...")
        return
    gender = "Boy 👨" if "boy" in update.message.text.lower() else "Girl 👩"
    if chat_id not in registered_users: registered_users[chat_id] = {}
    registered_users[chat_id][user.id] = {"username": f"@{user.username}", "gender": gender}
    await update.message.reply_text(f"✨ {gender} အဖြစ် မှတ်တမ်းတင်လိုက်ပြီနော် အချောလေး! 🥰")

def main():
    if not TOKEN: return
    keep_alive()
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_member))
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("bcast", broadcast))
    app.add_handler(CommandHandler(["boy", "girl"], register))
    app.add_handler(CommandHandler("love", love_match))
    app.add_handler(CommandHandler(["ban", "mute", "umute"], admin_tools))
    app.add_handler(MessageHandler(filters.ChatType.GROUPS & ~filters.COMMAND, lambda u, c: group_list.add(u.effective_chat.id)))
    
    app.run_polling()

if __name__ == '__main__': main()
              
