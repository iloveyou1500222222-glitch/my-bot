import logging, os, random
from flask import Flask
from threading import Thread
from telegram import Update, ChatPermissions
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- Keep Alive ---
app_flask = Flask('')
@app_flask.route('/')
def home(): return "မြနှင်း Bot Online ❤️"
def run(): app_flask.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
Thread(target=run, daemon=True).start()

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

# --- ✨ လူသစ်ဝင်လာရင် ချစ်စရာကြိုဆိုခြင်း ---
async def welcome_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.new_chat_members: return
    for member in update.message.new_chat_members:
        if member.id == context.bot.id: continue
        username = f"@{member.username}" if member.username else f"{member.first_name}"
        await update.message.reply_text(
            f"ဟယ်... အချောလေး {username} ရေ... 😍✨\n"
            f"ငါတို့ GP ထဲ ရောက်လာပြီဟယ်... ချောလိုက်တာနော် ချစ်စရာလေး။ 🥰💋\n"
            f"🎀 **မြနှင်း** ရဲ့ နွေးထွေးတဲ့ ရင်ခွင်ထဲကို ကြိုဆိုပါတယ်ရှင့်။ {AD_TEXT}", parse_mode='Markdown'
        )

# --- 🚫 Link Filter (Admin မဟုတ်ရင် ဖျက်မယ်) ---
async def link_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if await is_admin_or_owner(update, context): return
    if any(x in update.message.text.lower() for x in ["http", "https", "t.me"]):
        await update.message.delete()
        await update.message.reply_text(f"🚫 @{update.effective_user.username} ရေ... ဒီမှာ လင့်ခ်မချရဘူးလေကွာ... သဲလေး စိတ်ညစ်ရတယ်နော်! 🥺💔")

# --- 🎮 ဂိမ်းဖော်ရှာခြင်း ---
async def game_friend(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    cmd = update.message.text.lower()
    g_type = "mbb" if "mbb" in cmd else "pubg"
    if game_db[g_type]:
        partner_id, partner_name = game_db[g_type].pop()
        await update.message.reply_text(f"🎮 **ဂိမ်းဖော် တွေ့ပြီရှင့်!**\n@{user.username} နဲ့ @{partner_name} တို့ရေ... အတူတူ ဆော့လို့ရပြီနော်! 🎀✨")
    else:
        game_db[g_type].append((user.id, user.username))
        await update.message.reply_text(f"⏳ @{user.username} ရေ... {g_type.upper()} အဖော် ရှာပေးနေတယ်နော်... စောင့်ပေးပါဦးရှင့်! 🥺🙏")

# --- Start & Help (ဂိမ်းစနစ်ပါထည့်ထားတယ်) ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🎀 မင်္ဂလာပါရှင့် **မြနှင်း** ပါရှင့်။{AD_TEXT}", parse_mode='Markdown')

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_msg = (
        "✨ **မြနှင်း Bot အသုံးပြုနည်း** ✨\n\n"
        "👤 /boy , /girl - စာရင်းသွင်းရန်\n"
        "💖 /love - အတွဲချိတ်ရန်\n"
        "🎮 /mbbfriend - MLBB ဂိမ်းဖော်ရှာရန်\n"
        "🎮 /pubgfriend - PUBG ဂိမ်းဖော်ရှာရန်\n"
        "📢 /admin - Admin ခေါ်ရန်\n\n"
        "🛡 **Admin Tools**\n🚫 /ban , 🤫 /mute , 🔊 /umute"
    )
    await update.message.reply_text(help_msg)

# --- (ယခင်လုပ်ဆောင်ချက်များ - Register, Love, Admin Tools) ---
async def register(update, context):
    user = update.effective_user
    chat_id = update.effective_chat.id
    gender = "Boy 👨" if "boy" in update.message.text.lower() else "Girl 👩"
    if chat_id not in registered_users: registered_users[chat_id] = {}
    registered_users[chat_id][user.id] = {"username": f"@{user.username}", "gender": gender}
    await update.message.reply_text(f"✨ {gender} အဖြစ် မှတ်တမ်းတင်လိုက်ပြီနော်! 🥰")

async def love_match(update, context):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    if chat_id not in registered_users or user_id not in registered_users[chat_id]:
        await update.message.reply_text("🚨 အရင်ဆုံး /boy ဒါမှမဟုတ် /girl နဲ့ စာရင်းသွင်းပါဦး သဲလေးရဲ့... 🥺💗"); return
    me = registered_users[chat_id][user_id]
    potential = [uid for uid, data in registered_users[chat_id].items() if uid != user_id and data["gender"] != me["gender"]]
    if not potential: await update.message.reply_text("⏳ ဖူးစာရှင်လေးတွေ ရှာမတွေ့သေးဘူးရှင့်... 🥺💕"); return
    partner = registered_users[chat_id][random.choice(potential)]
    await update.message.reply_text(f"💘 **မြှားနတ်မောင် မြှားပစ်လိုက်ပြီရှင့်** 🏹\n❤️ {me['username']} ❤️ {partner['username']}\nမြန်မြန်လေး ညားကြပါစေရှင့်! 🥰", parse_mode='Markdown')

async def call_admin(update, context):
    admins = await context.bot.get_chat_administrators(update.effective_chat.id)
    mentions = " ".join([f"@{a.user.username}" for a in admins if a.user.username])
    await update.message.reply_text(f"📣📣 **Admin လေးတို့ရေ... သဲလေးတို့ အကူအညီလိုနေလို့ပါရှင်** 🥰\n{mentions}")

async def admin_tools(update, context):
    if not await is_admin_or_owner(update, context) or not update.message.reply_to_message: return
    target = update.message.reply_to_message.from_user
    cmd = update.message.text.lower()
    if '/ban' in cmd: await context.bot.ban_chat_member(update.effective_chat.id, target.id); await update.message.reply_text(f"🚨 @{target.username} ကို ထွက်သွားခိုင်းလိုက်ပါပြီ! 🤬")
    elif '/mute' in cmd: await context.bot.restrict_chat_member(update.effective_chat.id, target.id, ChatPermissions(can_send_messages=False)); await update.message.reply_text(f"🤫 @{target.username} ရေ... ခဏလေး အသံတိတ်ပေးပါဦးနော်! 🤐")
    elif '/umute' in cmd: await context.bot.restrict_chat_member(update.effective_chat.id, target.id, ChatPermissions(can_send_messages=True)); await update.message.reply_text(f"🔊 @{target.username} ကို ပြန်ချစ်ပေးလိုက်ပါပြီနော်! 😘")

# --- Main ---
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("admin", call_admin))
    app.add_handler(CommandHandler(["boy", "girl"], register))
    app.add_handler(CommandHandler("love", love_match))
    app.add_handler(CommandHandler(["mbbfriend", "pubgfriend"], game_friend))
    app.add_handler(CommandHandler(["ban", "mute", "umute"], admin_tools))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_member))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), link_filter))
    app.run_polling()

if __name__ == '__main__': main()
      
