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
    return "မြနှင်း Bot Online & Fully Functional!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app_flask.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- Settings & Data ---
TOKEN = os.environ.get("BOT_TOKEN") 
OWNER_ID = 7771663458  # သင့် ID ကို သော့ခတ်ထားပါတယ်
registered_users = {} 
group_list = set()  # Bot ရှိသမျှ Group ID တွေ မှတ်မယ့်နေရာ

BASE_LINK = "📢 https://t.me/Truelove150080"
CUSTOM_TEXT = "ရည်းစားရှာဖွေရေး gp ကို join ပေးကျပါရှင့် 🥰😘✅"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- ကြော်ငြာစာသား စနစ်တကျ ခေါ်ယူခြင်း ---
def get_ad_text():
    return f"\n\n━━━━━━━━━━━━━━\n{BASE_LINK} {CUSTOM_TEXT}"

# --- 🔐 Security: Admin & Owner Check ---
async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    if update.effective_chat.type == "private": return False
    user_id = update.effective_user.id
    if user_id == OWNER_ID: return True
    try:
        member = await context.bot.get_chat_member(update.effective_chat.id, user_id)
        return member.status in ['administrator', 'creator']
    except: return False

# --- 🚀 Broadcast System (Owner Only) ---
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("⛔ ဒီ Command ကို Bot ပိုင်ရှင်ပဲ သုံးခွင့်ရှိပါတယ်ရှင့်။")
        return
    
    if not update.message.reply_to_message:
        await update.message.reply_text("💡 ဖြန့်ချင်တဲ့ Post ကို Reply ပြန်ပြီး `/bcast` လို့ ရိုက်ပေးပါရှင့်။")
        return

    target_msg = update.message.reply_to_message
    success = 0
    await update.message.reply_text("📤 Bot ရှိသမျှ Group အကုန်လုံးဆီ ပို့စ်ဖြန့်ဝေခြင်း စတင်နေပါပြီ...")

    for chat_id in list(group_list):
        try:
            # Forward Tag မပါအောင် ပုံစံတူ ကူးယူပို့ပေးခြင်း
            await context.bot.copy_message(chat_id=chat_id, from_chat_id=update.effective_chat.id, message_id=target_msg.message_id)
            success += 1
        except:
            group_list.discard(chat_id)

    await update.message.reply_text(f"✅ စုစုပေါင်း Group ({success}) ခုဆီ ပို့စ်ဖြန့်ဝေပြီးပါပြီရှင့်။")

# --- Group ID များကို အလိုအလျောက် မှတ်သားခြင်း ---
async def track_groups(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type in ["group", "supergroup"]:
        group_list.add(update.effective_chat.id)

# --- ကြော်ငြာစာသား ပြင်ဆင်ခြင်း (/setad) ---
async def set_ad(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global CUSTOM_TEXT
    if update.effective_user.id != OWNER_ID: return
    if not context.args: return
    CUSTOM_TEXT = " ".join(context.args)
    await update.message.reply_text(f"✅ ကြော်ငြာစာသား ပြောင်းလဲမှု အောင်မြင်ပါပြီရှင့်!")

# --- Admin ခေါ်ရန် Command (/admin) ---
async def call_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == "private": return
    try:
        admins = await context.bot.get_chat_administrators(update.effective_chat.id)
        mentions = " ".join([f"@{a.user.username}" for a in admins if a.user.username])
        await update.message.reply_text(f"📣📣 Group Admin များရှင့် အကူအညီလိုအပ်နေပါသဖြင့် အမြန်လာရန် 🥰\n{mentions}" + get_ad_text())
    except: pass

# --- Register & Love Match (/boy, /girl, /love) ---
async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id
    cmd = update.message.text.split()[0].lower()
    
    if not user.username:
        await update.message.reply_text("❌ Username အရင်ဆောက်ပေးပါဦးနော် သဲလေး...")
        return
        
    gender = "Boy 👨" if "boy" in cmd else "Girl 👩"
    if chat_id not in registered_users: registered_users[chat_id] = {}
    registered_users[chat_id][user.id] = {"username": f"@{user.username}", "gender": gender}
    await update.message.reply_text(f"✨ {gender} အဖြစ် သတ်မှတ်ပြီးပါပြီ! /love နဲ့ ဖူးစာရှာကြည့်နော်... 🥰")

async def love_match(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    
    if chat_id not in registered_users or user_id not in registered_users[chat_id]:
        await update.message.reply_text("🚨 အရင်ဆုံး /boy ဒါမှမဟုတ် /girl နဲ့ စာရင်းသွင်းပါဦးရှင့်။")
        return
        
    me = registered_users[chat_id][user_id]
    potential = [uid for uid, data in registered_users[chat_id].items() if uid != user_id and data["gender"] != me["gender"]]
    
    if not potential:
        await update.message.reply_text("⏳ ဖူးစာရှင်လေးတွေ လမ်းမှာ ကားပိတ်နေလို့ ခဏစောင့်ပေးနော်... 🥺💗")
        return
        
    partner_id = random.choice(potential)
    partner_username = registered_users[chat_id][partner_id]["username"]
    
    # ⚠️ ဤနေရာတွင် စာလုံးမှား (get_and_text) ကို get_ad_text() ဟု မှန်ကန်စွာ ပြင်ဆင်ပြီးပါပြီ
    await update.message.reply_text(
        f"🎀 မြှားနတ်မောင်မြှားပစ်လိုက်ပါပီရှင့် 🎀\n\n"
        f"အတွဲလေးကတော့ {me['username']} နဲ့ {partner_username} တို့ပဲ ဖြစ်ပါတယ်ရှင့်! 🤪" + get_ad_text()
    )

# --- Start & Help ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type in ["group", "supergroup"]: 
        group_list.add(update.effective_chat.id)
    await update.message.reply_text("မဂ်လာပါရှင့် 😘\n🎀မြနှင်း🎀ကို Group ထဲထည့်ပေးနော်။ အာဘွား😘 သဲယေး👉🥺👈။\nအသုံးပြူပုံကြည့်ရန်--/help နှိပ်ပေးပါရှင့်..." + get_ad_text())

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_msg = "✨ *မြနှင်း Bot လမ်းညွှန်* ✨\n\n👤 /boy , /girl - စာရင်းသွင်း\n💖 /love - အတွဲချိတ်\n📢 /admin - Admin ခေါ်ရန်\n\n🛡 *Admin Tools*\n🚫 /ban , 🤫 /mute , 🔊 /umute\n\n⚙️ *Owner Only*\n🚀 /bcast - ပို့စ်ဖြန့်ဝေရန်"
    await update.message.reply_text(help_msg + get_ad_text(), parse_mode='Markdown')

# --- Admin Tools (Ban/Mute) ---
async def admin_tools(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context): return
    if not update.message.reply_to_message: return

    target = update.message.reply_to_message.from_user
    
    try:
        target_member = await context.bot.get_chat_member(update.effective_chat.id, target.id)
        if target_member.status in ['administrator', 'creator'] and update.effective_user.id != OWNER_ID:
            await update.message.reply_text("❌ Admin အချင်းချင်း လုပ်လို့မရပါဘူးရှင့်။")
            return
    except: pass

    cmd = update.message.text.split()[0].lower()
    try:
        if '/ban' in cmd:
            await context.bot.ban_chat_member(update.effective_chat.id, target.id)
            await update.message.reply_text(f"📣-သွားနင်ငါ gp ကထွက်သွား🤬🤬။ @{target.username} ကို Ban လိုက်ပါပီ 🎀😘")
        elif '/mute' in cmd:
            await context.bot.restrict_chat_member(update.effective_chat.id, target.id, ChatPermissions(can_send_messages=False))
            await update.message.reply_text(f"📣 စကားများလို့သဲယေးခနမြူတယ်ကွာ😘။ @{target.username} လေး ငြိမ်ငြိမ်နေနော်")
        elif '/umute' in cmd:
            await context.bot.restrict_chat_member(update.effective_chat.id, target.id, ChatPermissions(can_send_messages=True))
            await update.message.reply_text(f"📣 စကားပြန်ပြောလို့ရပီသဲယေး😘 @{target.username} စိတ်မဆိုးနဲ့နော် အာဘွား")
    except: 
        pass

# --- Main ---
def main():
    if not TOKEN: return
    keep_alive()
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("setad", set_ad))
    app.add_handler(CommandHandler("bcast", broadcast))
    app.add_handler(CommandHandler("admin", call_admin))
    app.add_handler(CommandHandler(["boy", "girl"], register))
    app.add_handler(CommandHandler("love", love_match))
    app.add_handler(CommandHandler(["ban", "mute", "umute"], admin_tools))
    
    # စာရိုက်သမျှ Group ID တွေ အလိုအလျောက် မှတ်သားရန်
    app.add_handler(MessageHandler(filters.ChatType.GROUPS & ~filters.COMMAND, track_groups))
    
    app.run_polling()

if __name__ == '__main__':
    main()
  
