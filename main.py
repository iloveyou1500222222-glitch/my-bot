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

# --- Settings ---
TOKEN = os.environ.get("BOT_TOKEN") 
OWNER_ID = 7771663458  
registered_users = {} 
group_list = set()  

# ✅ Video ID
WELCOME_VIDEO = "BAACAgUAAyEFAAT_ty-mAAIDemobPZxd25kTa7SNIjOF5_VhTZj7AAJuIAACyYXZVIh1A0X50n57OwQ" 

BASE_LINK = "📢 https://t.me/Truelove150080"
CUSTOM_TEXT = "ရည်းစားရှာဖွေရေး gp ကို join ပေးကျပါရှင့် 🥰😘✅"

logging.basicConfig(level=logging.INFO)

# --- 🔐 Security Check ---
async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    if update.effective_chat.type == "private": return False
    user_id = update.effective_user.id
    if user_id == OWNER_ID: return True
    try:
        member = await context.bot.get_chat_member(update.effective_chat.id, user_id)
        return member.status in ['administrator', 'creator']
    except: return False

# --- ✨ ကြိုဆိုခြင်း (နွဲ့နွဲ့လေး) ---
async def welcome_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        if member.id == context.bot.id:
            group_list.add(update.effective_chat.id)
            continue
            
        welcome_msg = (
            f"✨ **မင်္ဂလာပါ သဲလေး @{member.username or member.first_name}** ✨\n\n"
            f"**သဲလေးရေ လာ... အခန်းထဲလာ...** 🥰💋🍓\n\n"
            f"🎀 **မြနှင်း** ရဲ့ နွေးထွေးတဲ့ ရင်ခွင်ထဲကို ကြိုဆိုပါတယ်ရှင့်။ "
            f"ဒီမှာ ပျော်ပျော်ကြီး ဖူးစာရှာပါဦးနော်... အာဘွား! 😘"
        )
        
        try:
            await context.bot.send_video(
                chat_id=update.effective_chat.id,
                video=WELCOME_VIDEO,
                caption=welcome_msg,
                parse_mode='Markdown'
            )
        except:
            # ဗီဒီယို မရရင် စာပဲပို့မယ်
            await update.message.reply_text(welcome_msg, parse_mode='Markdown')

# --- 💖 Love Match (မြှားနတ်မောင် မြှားပစ်တဲ့အပိုင်း) ---
async def love_match(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    if chat_id not in registered_users or user_id not in registered_users[chat_id]:
        await update.message.reply_text("🚨 အရင်ဆုံး /boy ဒါမှမဟုတ် /girl နဲ့ စာရင်းသွင်းပါဦး သဲလေးရဲ့... 🥺💗")
        return
    
    me = registered_users[chat_id][user_id]
    potential = [uid for uid, data in registered_users[chat_id].items() if uid != user_id and data["gender"] != me["gender"]]
    
    if not potential:
        await update.message.reply_text("⏳ ဖူးစာရှင်လေးတွေ ရှာမတွေ့သေးဘူးရှင့်... ခဏစောင့်နော် အသည်းလေးတို့ 🥺💕")
        return
    
    partner_id = random.choice(potential)
    partner = registered_users[chat_id][partner_id]
    
    match_msg = (
        f"💘 **မြှားနတ်မောင် မြှားပစ်လိုက်ပြီရှင့်** 🏹🎯✨\n\n"
        f"🌹 **ကံပါလာတဲ့ အတွဲလေးကတော့** 🌹\n"
        f"┏━━━━━━━━━━━━━┓\n"
        f"   ❤️ {me['username']} \n"
        f"         ❌ \n"
        f"   ❤️ {partner['username']} \n"
        f"┗━━━━━━━━━━━━━┛\n\n"
        f"မြန်မြန်လေး အချစ်တွေ တိုးပြီး ညားကြပါစေရှင့်! 🤪🔥💕💋"
    )
    await update.message.reply_text(match_msg, parse_mode='Markdown')

# --- Start & Others ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type in ["group", "supergroup"]: group_list.add(update.effective_chat.id)
    msg = (
        f"မဂ်လာပါရှင့် 😘\n"
        f"🎀**မြနှင်း**🎀 Bot လေး အဆင်သင့်ရှိပါတယ်ရှင့်။\n"
        f"Group ထဲထည့်ပေးနော်။ အာဘွား😘 သဲယေး👉🥺👈\n\n"
        f"အသုံးပြူပုံကြည့်ရန် 👉 /help \n\n"
        f"━━━━━━━━━━━━━━\n"
        f"{BASE_LINK} \n{CUSTOM_TEXT}"
    )
    await update.message.reply_text(msg, parse_mode='Markdown')

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id
    if not user.username:
        await update.message.reply_text("❌ Username အရင်ဆောက်ပေးပါဦးနော် သဲလေး...")
        return
    cmd = update.message.text.lower()
    gender = "Boy 👨" if "boy" in cmd else "Girl 👩"
    if chat_id not in registered_users: registered_users[chat_id] = {}
    registered_users[chat_id][user.id] = {"username": f"@{user.username}", "gender": gender}
    await update.message.reply_text(f"✨ {gender} အဖြစ် သတ်မှတ်လိုက်ပြီနော် သဲလေး! 🥰🎀")

# --- 🛡 Admin Tools & Security ---
async def admin_tools(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context) or not update.message.reply_to_message: return
    target = update.message.reply_to_message.from_user
    cmd = update.message.text.lower()
    try:
        if '/ban' in cmd:
            await context.bot.ban_chat_member(update.effective_chat.id, target.id)
            await update.message.reply_text(f"📣 သွား... နင်ငါ့ GP က ထွက်သွားတော့! 🤬 @{target.username}")
        elif '/mute' in cmd:
            await context.bot.restrict_chat_member(update.effective_chat.id, target.id, ChatPermissions(can_send_messages=False))
            await update.message.reply_text(f"📣 စကားများလို့ ခဏမြူတယ်ကွာ... 😘 @{target.username}")
        elif '/umute' in cmd:
            await context.bot.restrict_chat_member(update.effective_chat.id, target.id, ChatPermissions(can_send_messages=True))
            await update.message.reply_text(f"📣 စကားပြန်ပြောလို့ရပြီ သဲလေးရေ... 😘 @{target.username}")
    except: pass

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID or not update.message.reply_to_message: return
    for chat_id in list(group_list):
        try: await context.bot.copy_message(chat_id=chat_id, from_chat_id=update.effective_chat.id, message_id=update.message.reply_to_message.message_id)
        except: group_list.discard(chat_id)
    await update.message.reply_text("✅ ဖြန့်ဝေပြီးပါပြီရှင့်။")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_msg = (
        "✨ **မြနှင်း Bot လမ်းညွှန်** ✨\n\n"
        "👤 /boy , /girl - စာရင်းသွင်းရန်\n"
        "💖 /love - ဖူးစာရှင်ရှာရန်\n"
        "📢 /admin - Admin ခေါ်ရန်\n\n"
        "🛡 **Admin Tools**\n"
        "🚫 /ban , 🤫 /mute , 🔊 /umute"
    )
    await update.message.reply_text(help_msg, parse_mode='Markdown')

def main():
    if not TOKEN: return
    keep_alive()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_member))
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("bcast", broadcast))
    app.add_handler(CommandHandler(["boy", "girl"], register))
    app.add_handler(CommandHandler("love", love_match))
    app.add_handler(CommandHandler(["ban", "mute", "umute"], admin_tools))
    app.add_handler(MessageHandler(filters.ChatType.GROUPS & ~filters.COMMAND, lambda u, c: group_list.add(u.effective_chat.id)))
    app.run_polling()

if __name__ == '__main__': main()
          
