import logging
import random
from telegram import Update, ChatPermissions
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- Settings ---
TOKEN = "8630120862:AAE-dAcieQOQMcKfjKgKLHdtEOi9nTtidyY"
OWNER_ID = 7771663458
AD_TEXT = "\n\n━━━━━━━━━━━━━━\n📢 ကြော်ငြာထည့်ရန် @Tear808 သို့သွားထည့်ပေးပါရှင့်💝✅"

# In-Memory Data
users_db = {}
waiting_boys = []
waiting_girls = []

# Logging setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- Admin Check Function ---
async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    if update.effective_chat.type == "private": return False
    user_id = update.effective_user.id
    if user_id == OWNER_ID: return True
    member = await context.bot.get_chat_member(update.effective_chat.id, user_id)
    return member.status in ['administrator', 'creator']

# --- Start & Help ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "မဂ်လာပါအသုံးပြုသူရှင့် 😘\n"
        "🎀မြနှင်း🎀ကိုGroupထဲထည့်ပေးနော်။အာဘွား😘သဲယေး👉🥺👈။\n"
        "အသုံပြုပုံကြည့်ရန်--/help ဟုနိပ်ပေးပါရှင့်။😘"
    )
    await update.message.reply_text(msg + AD_TEXT)

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
        "🔊 /umute - ပိတ်ထားတာ ပြန်ဖွင့်ရန်\n\n"
        "အကူအညီအတွက် ပိုင်ရှင် - @Tear808 ဆီသို့ 🎀"
    )
    await update.message.reply_text(help_text + AD_TEXT)

# --- Welcome Message ---
async def welcome_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        welcome_text = (
            f"မဂ်လာပါ {member.first_name} group ကနေ ကြိုဆိုပါတယ်နော်။ သဲယေး 🥰🤪\n"
            "ရည်းစားရှာရန်---\n"
            "boyဆိုပါက /boy ဟုရေးရန်။\n"
            "girlဆိုပါက /girl ဟုရေးရန်။\n"
            "ရေးပီးသွားပါက /love ဟုရေးပါရှင့် 😉"
        )
        await update.message.reply_text(welcome_text + AD_TEXT)

# --- Love Matching ---
async def set_gender(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    uname = update.effective_user.username or update.effective_user.first_name
    users_db[uid] = {"name": uname, "id": uid}
    cmd = update.message.text.lower()
    if "/boy" in cmd:
        if uid not in waiting_boys: waiting_boys.append(uid)
        await update.message.reply_text("ယောက်ျားလေးအဖြစ်သက်ဝင်ပါပီရှင့်😘။ရည်းစားရှာရန်/loveဟုရေးပါ")
    elif "/girl" in cmd:
        if uid not in waiting_girls: waiting_girls.append(uid)
        await update.message.reply_text("မိန်းခလေးအဖြစ်သက်ဝင်ပါပီရှင့်😘။ရည်းစားရှာရန်/loveဟုရေးပါ")

async def match(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not waiting_boys or not waiting_girls:
        await update.message.reply_text("⏳ လက်ရှိ စောင့်ဆိုင်းနေတဲ့ ဖူးစာဖက် မရှိသေးလို့ ခဏစောင့်ပေးပါနော် သဲလေး...")
        return
    b_id, g_id = waiting_boys.pop(0), waiting_girls.pop(0)
    b_name = f"@{users_db[b_id]['name']}"
    g_name = f"@{users_db[g_id]['name']}"
    await update.message.reply_text(f"📣 📣\n🎀မြှားနတ်မောင်မြှားပစ်လိုက်ပါပီရှင့်🎀\nမောင်({b_name})နှင့်မ({g_name})တိုသည်။ယနေမှစ၍တရားဝင်အတွဲများဖစ်သွားကြောင်း။🤪")

# --- Admin Tools ---
async def call_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_admins = await context.bot.get_chat_administrators(update.effective_chat.id)
    mentions = [f"@{a.user.username}" for a in chat_admins if a.user.username]
    if not mentions: mentions = ["Admin များ"]
    await update.message.reply_text(f"📣📣 Group ထဲတွင်ရှိကြကုန်သော {', '.join(mentions)} အကူအညီလိုအပ်နေပါသဖြင့် Gp သို့အမြန်လာရန်။ 😊")

async def admin_tools(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context): return
    if not update.message.reply_to_message: return
    target = update.message.reply_to_message.from_user
    cmd = update.message.text.split()[0].lower()
    
    if '/ban' in cmd:
        await context.bot.ban_chat_member(update.effective_chat.id, target.id)
        await update.message.reply_text(f"📣📣-သွားနင်ငါgpကထွက်သွား🤬🤬။ @{target.username} ကိုBanလိုက်ပါပီGpမှ🎀😘🎀")
    elif '/mute' in cmd:
        await context.bot.restrict_chat_member(update.effective_chat.id, target.id, ChatPermissions(can_send_messages=False))
        await update.message.reply_text(f"📣📣စကားများလို့သဲယေးခနမြူတယ်ကွာ😘။ @{target.username} ကိုမြူလိုက်ပြီ")
    elif '/umute' in cmd:
        await context.bot.restrict_chat_member(update.effective_chat.id, target.id, ChatPermissions(can_send_messages=True, can_send_media_messages=True))
        await update.message.reply_text(f"📣📣စကားပြန်ပြောလို့ရပီသဲယေး😘 @{target.username} ကို Unmute လုပ်ပေးလိုက်ပြီ🎀")

# --- Main App ---
def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler(["boy", "girl"], set_gender))
    app.add_handler(CommandHandler("love", match))
    app.add_handler(CommandHandler("admin", call_admin))
    app.add_handler(CommandHandler(["ban", "mute", "umute"], admin_tools))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_member))
    
    print("🚀 Bot is starting...")
    app.run_polling()

if __name__ == '__main__':
    main()
  
