import logging
import os
from flask import Flask
from threading import Thread
from telegram import Update, ChatPermissions
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- Keep Alive System (Render အတွက် ပိုမိုကောင်းမွန်အောင် ပြင်ဆင်ထားသည်) ---
app_flask = Flask('')

@app_flask.route('/')
def home():
    return "Bot is alive and running!"

def run():
    # Render ရဲ့ Dynamic Port ကို ဖတ်ပြီး မောင်းနှင်ရန် ပြင်ဆင်ထားသည်
    port = int(os.environ.get("PORT", 8080))
    app_flask.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- Settings ---
TOKEN = "8630120862:AAH1uoBp0jg9sei-V3chfkwAd3yzlpjdf9o"
OWNER_ID = 7771663458

# ကြော်ငြာစာသား အသစ်ပြင်ဆင်ထားမှု 👇
AD_TEXT = "\n\n━━━━━━━━━━━━━━\n📢 https://t.me/Truelove150080 ရည်းစားရှာဖွေရေး gp ကို join ပေးကျပါရှင့် 🥰😘✅"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- Admin Check ---
async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    if update.effective_chat.type == "private": return False
    user_id = update.effective_user.id
    if user_id == OWNER_ID: return True
    member = await context.bot.get_chat_member(update.effective_chat.id, user_id)
    return member.status in ['administrator', 'creator']

# --- Bot Logic ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "မဂ်လာပါအသုံးပြုသူရှင့် 😘\n"
        "🎀မြနှင်း🎀ကို Group ထဲထည့်ပေးနော်။ အာဘွား😘 သဲယေး👉🥺👈။\n"
        "အသုံးပြူပုံကြည့်ရန်--/help ဟုနှိပ်ပေးပါရှင့်။😘"
    )
    await update.message.reply_text(msg + AD_TEXT)

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "✨ *Bot အသုံးပြုနည်းလမ်းညွှန်* ✨\n\n"
        "👤 /boy , /girl - စာရင်းသွင်းရန်\n"
        "💖 /love - အတွဲချိတ်ရန်\n"
        "📢 /admin - Admin ခေါ်ရန်\n\n"
        "🛡 *Admin Tools*\n"
        "🚫 /ban , 🤫 /mute , 🔊 /umute\n\n"
        "အကူအညီအတွက် ပိုင်ရှင် - @Tear808 ဆီသို့ 🎀"
    )
    await update.message.reply_text(help_text + AD_TEXT)

async def call_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    admins = await context.bot.get_chat_administrators(update.effective_chat.id)
    mentions = ", ".join([f"@{a.user.username}" for a in admins if a.user.username])
    await update.message.reply_text(f"📣📣 Group Admin များဖြစ်သော {mentions or 'Admin များ'} အကူအညီလာပေးပါဦးရှင့်! 😊" + AD_TEXT)

async def admin_tools(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context) or not update.message.reply_to_message: return
    target = update.message.reply_to_message.from_user
    cmd = update.message.text.split()[0].lower()
    
    if '/ban' in cmd:
        await context.bot.ban_chat_member(update.effective_chat.id, target.id)
        await update.message.reply_text(f"📣📣-သွားနင်ငါ gp ကထွက်သွား🤬🤬။ @{target.username} ကို Ban လိုက်ပါပီ 🎀😘🎀")
    elif '/mute' in cmd:
        await context.bot.restrict_chat_member(update.effective_chat.id, target.id, ChatPermissions(can_send_messages=False))
        await update.message.reply_text(f"📣📣 စကားများလို့သဲယေးခနမြူတယ်ကွာ😘။ @{target.username} ကို မြူလိုက်ပြီ")
    elif '/umute' in cmd:
        await context.bot.restrict_chat_member(update.effective_chat.id, target.id, ChatPermissions(can_send_messages=True))
        await update.message.reply_text(f"📣📣 စကားပြန်ပြောလို့ရပီသဲယေး😘 @{target.username} ကို Unmute လုပ်ပေးလိုက်ပြီ🎀")

# --- Main Setup ---
def main():
    keep_alive() # Render မှာ Run ဖို့ Flask ကို နှိုးခြင်း
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("admin", call_admin))
    app.add_handler(CommandHandler(["ban", "mute", "umute"], admin_tools))
    
    print("🚀 Bot is starting with New Ad...")
    app.run_polling()

if __name__ == '__main__':
    main()
