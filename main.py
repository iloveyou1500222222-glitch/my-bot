import logging
from telegram import Update, ChatPermissions
from telegram.ext import Application, CommandHandler, ContextTypes

# --- Settings ---
TOKEN = "8630120862:AAE-dAcieQOQMcKfjKgKLHdtEOi9nTtidyY"
AD_TEXT = "\n\n📢 ကြော်ငြာထည့်ရန် @Tear808 သို့သွားထည့်ပေးပါရှင့်💝✅"

# In-Memory Data
users_db = {}
waiting_boys = []
waiting_girls = []

logging.basicConfig(level=logging.INFO)

# --- Admin Check Function ---
async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Gp ထဲက Admin တိုင်းကို စစ်ဆေးပေးသည်"""
    user_id = update.effective_user.id
    # Bot ပိုင်ရှင်ကို အမြဲခွင့်ပြုသည်
    if user_id == 7771663458: return True
    
    member = await context.bot.get_chat_member(update.effective_chat.id, user_id)
    return member.status in ['administrator', 'creator']

# --- Bot Logic ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "မဂ်လာပါအသုံးပြုသူရှင့် 😘\n🎀မြနှင်း🎀ကိုGroupထဲထည့်ပေးနော်။အာဘွား😘သဲယေး👉🥺👈။ချစ်တယ်။😘"
    await update.message.reply_text(msg + AD_TEXT)

async def set_gender(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    uname = update.effective_user.username or update.effective_user.first_name
    users_db[uid] = {"name": uname, "id": uid}
    if "/boy" in update.message.text:
        if uid not in waiting_boys: waiting_boys.append(uid)
        await update.message.reply_text("ယောက်ျားလေးအဖြစ်သက်ဝင်ပါပီရှင့်😘။ရည်းစားရှာရန်/loveဟုရေးပါ")
    elif "/girl" in update.message.text:
        if uid not in waiting_girls: waiting_girls.append(uid)
        await update.message.reply_text("မိန်းခလေးအဖြစ်သက်ဝင်ပါပီရှင့်😘။ရည်းစားရှာရန်/loveဟုရေးပါ")

async def match(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not waiting_boys or not waiting_girls:
        await update.message.reply_text("တွဲရန် လူမလုံလောက်သေးပါ။")
        return
    b_name = f"@{users_db[waiting_boys.pop(0)]['name']}"
    g_name = f"@{users_db[waiting_girls.pop(0)]['name']}"
    await update.message.reply_text(f"📣 📣\n🎀မြှားနတ်မောင်မြှားပစ်လိုက်ပါပီရှင့်🎀\nမောင်({b_name})နှင့်မ({g_name})တိုသည်။ယနေမှစ၍တရားဝင်အတွဲများဖစ်သွားကြောင်း။🤪")

async def call_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Group ထဲက Admin အားလုံးကို ရှာပြီး @ ခေါ်ခြင်း"""
    chat_admins = await context.bot.get_chat_administrators(update.effective_chat.id)
    mentions = [f"@{a.user.username}" for a in chat_admins if a.user.username]
    if not mentions: mentions = ["Admin များ"]
    await update.message.reply_text(f"📣📣 Group ထဲတွင်ရှိကြကုန်သော {', '.join(mentions)} အကူအညီလိုအပ်နေပါသဖြင့် Gp သို့အမြန်လာရန်။ 😊")

async def admin_tools(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context): return
    if not update.message.reply_to_message: return
    
    target = update.message.reply_to_message.from_user
    cmd = update.message.text.split()[0]
    
    if cmd == '/ban':
        await context.bot.ban_chat_member(update.effective_chat.id, target.id)
        await update.message.reply_text(f"📣📣-သွားနင်ငါgpကထွက်သွား🤬🤬။ @{target.username} ကိုBanလိုက်ပါပီ🎀😘🎀")
    elif cmd == '/mute':
        await context.bot.restrict_chat_member(update.effective_chat.id, target.id, ChatPermissions(can_send_messages=False))
        await update.message.reply_text(f"📣📣စကားများလို့သဲယေးခနမြူတယ်ကွာ😘။ @{target.username} ကိုမြူလိုက်ပြီ")
    elif cmd == '/umute':
        await context.bot.restrict_chat_member(update.effective_chat.id, target.id, ChatPermissions(can_send_messages=True))
        await update.message.reply_text(f"📣📣စကားပြန်ပြောလို့ရပီသဲယေး😘 @{target.username} ကို Unmute လုပ်ပေးလိုက်ပြီ🎀")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler(["boy", "girl"], set_gender))
    app.add_handler(CommandHandler("love", match))
    app.add_handler(CommandHandler("admin", call_admin))
    app.add_handler(CommandHandler(["ban", "mute", "umute"], admin_tools))
    app.run_polling()
# --- Help Command ---
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "✨ *Bot အသုံးပြုနည်းလမ်းညွှန်* ✨\n\n"
        "👤 /boy - ယောက်ျားလေးအဖြစ် စာရင်းသွင်းရန်\n"
        "👧 /girl - မိန်းကလေးအဖြစ် စာရင်းသွင်းရန်\n"
        "💖 /love - အတွဲချိတ်ရန်\n"
        "📢 /admin - Admin များကို ခေါ်ရန်\n\n"
        "🛡 *Admin Tool များ (Reply လုပ်ပြီးသုံးပါ)*\n"
        "🚫 /ban - Group မှ ထုတ်ရန်\n"
        "🤫 /mute - စကားပြောမရအောင် ပိတ်ရန်\n"
        "🔊 /umute - ပိတ်ထားတာ ပြန်ဖွင့်ရန်"
    )
    await update.message.reply_text(help_text + AD_TEXT, parse_mode="Markdown")

f _n __name__ == '__main__':
    main()
  
