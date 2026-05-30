import logging
import os
import random
from flask import Flask
from threading import Thread
from telegram import Update, ChatPermissions
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- Keep Alive System (Render 24/7 Run ရန်) ---
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

# --- 🛡️ လုံခြုံရေးအတွက် စနစ်များ ---
# Token ကို Code ထဲမှာ အသေသေချာချာ ဖုံးကွယ်ထားပါတယ် (အဟက်မခံရအောင်)
TOKEN = os.environ.get("BOT_TOKEN") 
OWNER_ID = 7771663458

# 👥 အတွဲချိတ်ရန်အတွက် စာရင်းသိမ်းဆည်းမည့် နေရာ
registered_users = {} 

# 📢 ကြော်ငြာစာသား
AD_TEXT = "\n\n━━━━━━━━━━━━━━\n📢 https://t.me/Truelove150080 ရည်းစားရှာဖွေရေး gp ကို join ပေးကျပါရှင့် 🥰😘✅"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- Admin စစ်ဆေးသည့် စနစ် ---
async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    if update.effective_chat.type == "private": return False
    user_id = update.effective_user.id
    if user_id == OWNER_ID: return True
    try:
        member = await context.bot.get_chat_member(update.effective_chat.id, user_id)
        return member.status in ['administrator', 'creator']
    except:
        return False

# --- 👤 စာရင်းသွင်းခြင်း (/boy , /girl) ---
async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id
    cmd = update.message.text.split()[0].lower()
    
    if not user.username:
        await update.message.reply_text("❌ သဲလေး... အတွဲချိတ်ဖို့အတွက် Telegram Settings ထဲမှာ Username (ဥပမာ- @name) အရင်ဆောက်ပေးပါဦးနော် 🥺")
        return

    gender = "Boy 👨" if "boy" in cmd else "Girl 👩"
    
    if chat_id not in registered_users:
        registered_users[chat_id] = {}
        
    registered_users[chat_id][user.id] = {
        "username": f"@{user.username}",
        "gender": gender
    }
    
    await update.message.reply_text(f"✨ အောင်သွယ်တော် မြနှင်းဆီမှာ {gender} အဖြစ် စာရင်းသွင်းအောင်မြင်သွားပါပြီရှင့်! 💖\nအခုပဲ /love လို့ရိုက်ပြီး ဖူးစာရှာကြည့်လိုက်တော့နော်... 🥰")

# --- 💖 အတွဲချိတ်ပေးခြင်း (/love) ---
async def love_match(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id
    
    # Register မလုပ်ရသေးရင် ချိတ်မပေးပါ
    if chat_id not in registered_users or user.id not in registered_users[chat_id]:
        await update.message.reply_text("🚨 သဲလေးက စာရင်းမသွင်းရသေးဘူးလေ... အရင်ဆုံး /boy သို့မဟုတ် /girl လို့ ရိုက်ပြီး စာရင်းသွင်းပေးနော်... 😘")
        return

    my_gender = registered_users[chat_id][user.id]["gender"]
    
    # ကိုယ်နဲ့ လိင်မတူတဲ့သူတွေကို ရှာမယ်
    potential_partners = [
        uid for uid, data in registered_users[chat_id].items()
        if uid != user.id and data["gender"] != my_gender
    ]

    # စာသားလှလှလေး ထည့်ထားသည့်နေရာ 👇
    if not potential_partners:
        await update.message.reply_text("⏳ အိုး... ဖူးစာရှင်လေးက လမ်းမှာ ကားပိတ်နေလို့လားမသိဘူး... ခဏလေး စောင့်ပေးနော် သဲလေး။ တစ်ယောက်ယောက် /love လို့ ရိုက်လိုက်ရင် ချက်ချင်း ချိတ်ပေးမယ်နော်... 🥺💗")
        return

    # ကျပန်းတစ်ယောက်ကို ရွေးချယ်ပြီး ချိတ်ပေးခြင်း
    partner_id = random.choice(potential_partners)
    partner_username = registered_users[chat_id][partner_id]["username"]

    await update.message.reply_text(
        f"🎉 ဝိုး... ရင်ခုန်စရာ အတွဲလေး ချိတ်မိသွားပါပြီရှင်! ✨\n\n"
        f"သင့်ရဲ့ ဖူးစာဖက်လေးကတော့ 👉 {partner_username} ပါတဲ့။\n\n"
        f"ပျော်ရွှင်စရာ အချိန်လေးတွေ ပိုင်ဆိုင်ပါစေနော်... 👩‍❤️‍👨💞 {AD_TEXT}"
    )

# --- Base Commands ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "မဂ်လာပါအသုံးပြုသူရှင့် 😘\n🎀မြနှင်း🎀ကို Group ထဲထည့်ပေးနော်။ အာဘွား😘 သဲယေး👉🥺👈။\nအသုံးပြူပုံကြည့်ရန်--/help ဟုနှိပ်ပေးပါရှင့်။😘"
    await update.message.reply_text(msg + AD_TEXT)

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = "✨ *Bot အသုံးပြုနည်းလမ်းညွှန်* ✨\n\n👤 /boy , /girl - စာရင်းသွင်းရန်\n💖 /love - အတွဲချိတ်ရန်\n📢 /admin - Admin ခေါ်ရန်\n\n🛡 *Admin Tools*\n🚫 /ban , 🤫 /mute , 🔊 /umute\n\nအကူအညီအတွက် ပိုင်ရှင် - @Tear808 ဆီသို့ 🎀"
    await update.message.reply_text(help_text + AD_TEXT, parse_mode='Markdown')

async def admin_tools(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context) or not update.message.reply_to_message: return
    target = update.message.reply_to_message.from_user
    cmd = update.message.text.split()[0].lower()
    
    try:
        if '/ban' in cmd:
            await context.bot.ban_chat_member(update.effective_chat.id, target.id)
            await update.message.reply_text(f"📣📣-သွားနင်ငါ gp ကထွက်သွား🤬🤬။ @{target.username} ကို Ban လိုက်ပါပီ 🎀😘🎀")
        elif '/mute' in cmd:
            await context.bot.restrict_chat_member(update.effective_chat.id, target.id, ChatPermissions(can_send_messages=False))
            await update.message.reply_text(f"📣📣 စကားများလို့သဲယေးခနမြူတယ်ကွာ😘။ @{target.username} ကို မြူလိုက်ပြီ")
        elif '/umute' in cmd:
            await context.bot.restrict_chat_member(update.effective_chat.id, target.id, ChatPermissions(can_send_messages=True))
            await update.message.reply_text(f"📣📣 စကားပြန်ပြောလို့ရပီသဲယေး😘 @{target.username} ကို Unmute လုပ်ပေးလိုက်ပြီ🎀")
    except:
        await update.message.reply_text("Error: Bot ကို Admin အာဏာအပြည့်ပေးထားဖို့ လိုပါတယ်ရှင့်။")

# --- Main Runtime ---
def main():
    if not TOKEN:
        print("❌ Error: BOT_TOKEN ကို Hosting Setting ထဲမှာ မထည့်ရသေးပါ!")
        return

    keep_alive()
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler(["boy", "girl"], register))
    app.add_handler(CommandHandler("love", love_match))
    app.add_handler(CommandHandler(["ban", "mute", "umute"], admin_tools))
    
    print("🚀 Bot ကို လုံခြုံရေးအပြည့်ဖြင့် မောင်းနှင်နေပါပြီ...")
    app.run_polling()

if __name__ == '__main__':
    main()
      
