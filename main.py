import logging
import os
import random
from flask import Flask
from threading import Thread
from telegram import Update, ChatPermissions
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- Keep Alive System ---
app_flask = Flask('')

@app_flask.route('/')
def home():
    return "မြနှင်း Bot စနစ် ကောင်းမွန်စွာ လည်ပတ်နေပါသည်!"

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
AD_TEXT = "\n\n━━━━━━━━━━━━━━\n📢 https://t.me/Truelove150080 ရည်းစားရှာဖွေရေး gp ကို join ပေးကျပါရှင့် 🥰😘✅"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- Admin Check ---
async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    if update.effective_chat.type == "private": return False
    user_id = update.effective_user.id
    if user_id == OWNER_ID: return True
    try:
        member = await context.bot.get_chat_member(update.effective_chat.id, user_id)
        return member.status in ['administrator', 'creator']
    except: return False

# --- Admin ခေါ်ရန် Command (/admin) ---
async def call_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == "private":
        await update.message.reply_text("ဒီ Command ကို Group ထဲမှာပဲ သုံးလို့ရပါတယ်ရှင့်။")
        return
    
    try:
        admins = await context.bot.get_chat_administrators(update.effective_chat.id)
        # username ရှိတဲ့ admin တွေကိုပဲ mention ခေါ်ပါမယ်
        mentions = " ".join([f"@{a.user.username}" for a in admins if a.user.username])
        
        await update.message.reply_text(
            f"📣📣 အရေးပေါ်သတင်း!!!\nGroup Admin များဖြစ်ကြသော {mentions or 'Admin များ'} အကူအညီလာပေးပါဦးရှင့်! ✨🥰" + AD_TEXT
        )
    except Exception as e:
        await update.message.reply_text("Admin တွေကို ခေါ်လို့မရဖြစ်နေပါတယ်ရှင့်။ Bot ကို Admin Permission ပေးထားပါဦး။")

# --- Register (/boy, /girl) ---
async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id
    cmd = update.message.text.split()[0].lower()
    
    if not user.username:
        await update.message.reply_text("❌ သဲလေး... အတွဲချိတ်ဖို့အတွက် Telegram Settings မှာ Username အရင်ဆောက်ပေးပါဦးနော် 🥺")
        return

    gender = "Boy 👨" if "boy" in cmd else "Girl 👩"
    if chat_id not in registered_users: registered_users[chat_id] = {}
    registered_users[chat_id][user.id] = {"username": f"@{user.username}", "gender": gender}
    
    await update.message.reply_text(f"✨ မြနှင်းဆီမှာ {gender} အဖြစ် စာရင်းသွင်းပြီးပါပြီ! /love နဲ့ ဖူးစာရှာကြည့်နော်... 🥰")

# --- Love Match (/love) ---
async def love_match(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id
    
    if chat_id not in registered_users or user.id not in registered_users[chat_id]:
        await update.message.reply_text("🚨 အရင်ဆုံး /boy ဒါမှမဟုတ် /girl နဲ့ စာရင်းသွင်းပေးပါဦး သဲလေးရဲ့... 😘")
        return

    my_gender = registered_users[chat_id][user.id]["gender"]
    potential_partners = [uid for uid, data in registered_users[chat_id].items() if uid != user.id and data["gender"] != my_gender]

    if not potential_partners:
        await update.message.reply_text("⏳ အိုး... ဖူးစာရှင်လေးက လမ်းမှာ ကားပိတ်နေလို့လားမသိဘူး... ခဏလေး စောင့်ပေးနော် သဲလေး။ တစ်ယောက်ယောက် /love လို့ ရိုက်လိုက်ရင် ချက်ချင်း ချိတ်ပေးမယ်နော်... 🥺💗")
        return

    partner_id = random.choice(potential_partners)
    partner_username = registered_users[chat_id][partner_id]["username"]

    await update.message.reply_text(
        f"🎉 ဝိုး... ရင်ခုန်စရာ အတွဲလေး ချိတ်မိသွားပါပြီရှင်! ✨\n\n"
        f"သင့်ရဲ့ ဖူးစာဖက်လေးကတော့ 👉 {partner_username} ပါတဲ့။\n\n"
        f"ပျော်ရွှင်စရာ အချိန်လေးတွေ ပိုင်ဆိုင်ပါစေနော်... 👩‍❤️‍👨💞 {AD_TEXT}"
    )

# --- Start & Help ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("မဂ်လာပါရှင့် 😘\n🎀မြနှင်း🎀ကို Group ထဲထည့်ပေးနော်။ အာဘွား😘 သဲယေး👉🥺👈။\nအသုံးပြူပုံကြည့်ရန်--/help နှိပ်ပေးပါရှင့်။" + AD_TEXT)

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = "✨ *မြနှင်း Bot လမ်းညွှန်* ✨\n\n👤 /boy , /girl - စာရင်းသွင်း\n💖 /love - အတွဲချိတ်\n📢 /admin - Admin ခေါ်ရန်\n\n🛡 *Admin Tools*\n🚫 /ban , 🤫 /mute , 🔊 /umute"
    await update.message.reply_text(help_text + AD_TEXT, parse_mode='Markdown')

# --- Admin Tools (Ban/Mute) ---
async def admin_tools(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context) or not update.message.reply_to_message: return
    target = update.message.reply_to_message.from_user
    cmd = update.message.text.split()[0].lower()
    
    try:
        if '/ban' in cmd:
            await context.bot.ban_chat_member(update.effective_chat.id, target.id)
            await update.message.reply_text(f"📣-သွားနင်ငါ gp ကထွက်သွား🤬🤬။ @{target.username} ကို Ban လိုက်ပါပီ 🎀😘")
        elif '/mute' in cmd:
            await context.bot.restrict_chat_member(update.effective_chat.id, target.id, ChatPermissions(can_send_messages=False))
            await update.message.reply_text(f"📣 စကားများလို့သဲယေးခနမြူတယ်ကွာ😘။ @{target.username} ကို မြူလိုက်ပြီ")
        elif '/umute' in cmd:
            await context.bot.restrict_chat_member(update.effective_chat.id, target.id, ChatPermissions(can_send_messages=True))
            await update.message.reply_text(f"📣 စကားပြန်ပြောလို့ရပီသဲယေး😘 @{target.username} ကို Unmute လုပ်ပေးလိုက်ပြီ")
    except: pass

# --- Main ---
def main():
    if not TOKEN: return
    keep_alive()
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("admin", call_admin)) # ဒီ Command အသစ်ထည့်ထားပါတယ်
    app.add_handler(CommandHandler(["boy", "girl"], register))
    app.add_handler(CommandHandler("love", love_match))
    app.add_handler(CommandHandler(["ban", "mute", "umute"], admin_tools))
    
    app.run_polling()

if __name__ == '__main__':
    main()
  
