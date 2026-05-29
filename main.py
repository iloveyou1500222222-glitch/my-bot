import os
import random
import logging
from dotenv import load_dotenv
from telegram import Update, ChatPermissions
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.error import TelegramError

# .env ဖိုင်မှ Token ကို လုံခြုံစွာ ဖတ်ယူခြင်း
load_dotenv()
TOKEN = os.getenv("8630120862:AAH9XF5rSoz7-rrVkkeOV3gjWqP5mqyD5a0")

# ရိုးရှင်းပြီး စိတ်ချရတဲ့ In-Memory Database (Bot ပိတ်ရင် Reset ဖြစ်ပါမယ်၊ ပိုလုံခြုံပါတယ်)
users_db = {}  # {user_id: {"gender": "boy"/"girl", "username": "..."}}
waiting_boys = set()
waiting_girls = set()

# ကြော်ငြာစာသား (ဒီနေရာမှာ စာသားကို လိုသလို ပြောင်းနိုင်ပါတယ်)
AD_TEXT = "\n\n📢 ကြော်ငြာထည့်ရန် @Tear808 သို့သွားထည့်ပေးပါရှင့်💝✅"

# Logging သတ်မှတ်ခြင်း (Error ရှာရလွယ်ကူစေရန်)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# ================== USER FUNCTIONS ==================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    chat_type = update.effective_chat.type
    
    if chat_type == "private":
        welcome_msg = f"မင်္ဂလာပါရှင့် အသုံးပြုသူ {user_name}။" + AD_TEXT
        await update.message.reply_text(welcome_msg)
    else:
        await update.message.reply_text(f"မင်္ဂလာပါ {user_name} သဲလေးရေ! Gp ထဲ ရောက်လာလို့ ကြိုဆိုပါတယ်ရှင့်။ 😘")

async def set_boy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.username or "No Username"
    
    users_db[user_id] = {"gender": "boy", "username": username}
    # အကယ်၍ မိန်းကလေးစာရင်းထဲရှိနေရင် ဖျက်မယ်
    waiting_girls.discard(user_id)
    waiting_boys.add(user_id)
    
    await update.message.reply_text("👦 သင့်ကို 'ယောက်ျားလေး' အဖြစ် မှတ်ပုံတင်လိုက်ပါပြီ။ /love နဲ့ အတွဲရှာနိုင်ပါပြီ။")

async def set_girl(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.username or "No Username"
    
    users_db[user_id] = {"gender": "girl", "username": username}
    # အကယ်၍ ယောက်ျားလေးစာရင်းထဲရှိနေရင် ဖျက်မယ်
    waiting_boys.discard(user_id)
    waiting_girls.add(user_id)
    
    await update.message.reply_text("👧 သင့်ကို 'မိန်းကလေး' အဖြစ် မှတ်ပုံတင်လိုက်ပါပြီ။ /love နဲ့ အတွဲရှာနိုင်ပါပြီ။")

async def match_love(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if user_id not in users_db:
        await update.message.reply_text("❌ အရင်ဆုံး မိမိ Gender ကို သတ်မှတ်ပေးပါ။\nယောက်ျားလေးဆိုရင် /boy\nမိန်းကလေးဆိုရင် /girl ဟု ရိုက်ပါနော်။")
        return

    user_gender = users_db[user_id]["gender"]
    
    if user_gender == "boy":
        if not waiting_girls:
            waiting_boys.add(user_id)
            await update.message.reply_text("⏳ လက်ရှိ စောင့်ဆိုင်းနေတဲ့ မိန်းကလေးမရှိသေးလို့ ခဏစောင့်ပေးပါနော် သဲလေး...")
            return
        # ကျပန်း အတွဲချိတ်ပေးခြင်း
        partner_id = random.choice(list(waiting_girls))
        waiting_girls.remove(partner_id)
        waiting_boys.discard(user_id)
    else:
        if not waiting_boys:
            waiting_girls.add(user_id)
            await update.message.reply_text("⏳ လက်ရှိ စောင့်ဆိုင်းနေတဲ့ ယောက်ျားလေးမရှိသေးလို့ ခဏစောင့်ပေးပါနော် သဲလေး...")
            return
        # ကျပန်း အတွဲချိတ်ပေးခြင်း
        partner_id = random.choice(list(waiting_boys))
        waiting_boys.remove(partner_id)
        waiting_girls.discard(user_id)

    # အတွဲရသွားပြီဖြစ်ကြောင်း အကြောင်းကြားစာ
    partner_info = users_db[partner_id]
    partner_username = f"@{partner_info['username']}" if partner_info['username'] != "No Username" else f"ID: {partner_id}"
    
    await update.message.reply_text(f"🎉 ဝိုး... အတွဲချိတ်မိသွားပါပြီရှင်!\n\nသင့်ဖူးစာဖက်ကတော့ 👉 {partner_username} ဖြစ်ပါတယ်ရှင့်။ သွားရောက် Chat နိုင်ပါပြီ။ {AD_TEXT}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "🤖 **Bot အသုံးပြုနည်း လမ်းညွှန်**\n\n"
        "✨ **အတွဲချိတ်ရန်**\n"
        "/boy - မိမိကိုယ်ကို ယောက်ျားလေးအဖြစ် သတ်မှတ်ရန်\n"
        "/girl - မိမိကိုယ်ကို မိန်းကလေးအဖြစ် သတ်မှတ်ရန်\n"
        "/love - ကျပန်း ဖူးစာဖက် အတွဲချိတ်ရန်\n\n"
        "🛡️ **Group Admin စနစ် (Admin များသာ)**\n"
        "👉 (Ban/Mute ချင်သူ၏ Message ကို Reply ပြန်၍ သုံးပါ)\n"
        "/ban - အဖွဲ့ဝင်ကို Group ထဲမှ အပြီးပိုင် ထုတ်ပစ်ရန်\n"
        "/mute - အဖွဲ့ဝင်ကို စာရေးခွင့် ပိတ်ရန်\n"
        "/admin - Group ထဲရှိ Admin အားလုံးကို Tag ခေါ်ရန်"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")

# ================== ADMIN FUNCTIONS (GROUP) ==================

async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """လုံခြုံရေးအတွက် Command သုံးသူသည် တကယ့် Admin ဟုတ်မဟုတ် စစ်ဆေးခြင်း"""
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    member = await context.bot.get_chat_member(chat_id, user_id)
    return member.status in ['administrator', 'creator']

async def ban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        return  # Admin မဟုတ်ရင် ဘာမှမလုပ်ဘူး (လုံခြုံရေးအရ)
        
    if update.message.reply_to_message:
        target_user = update.message.reply_to_message.from_user
        try:
            await context.bot.ban_chat_member(chat_id=update.effective_chat.id, user_id=target_user.id)
            await update.message.reply_text(f"🛑 {target_user.first_name} ကို Group ထဲကနေ မောင်းထုတ်လိုက်ပါပြီ။")
        except TelegramError:
            await update.message.reply_text("❌ Bot မှာ Ban ဖို့ အခွင့်အာဏာ (Permission) မရှိသေးပါဘူး။")
    else:
        await update.message.reply_text("❌ Ban ချင်တဲ့သူရဲ့စာကို Reply ပြန်ပြီး /ban လို့ ရိုက်ပေးပါ။")

async def mute_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        return
        
    if update.message.reply_to_message:
        target_user = update.message.reply_to_message.from_user
        permissions = ChatPermissions(can_send_messages=False)
        try:
            await context.bot.restrict_chat_member(chat_id=update.effective_chat.id, user_id=target_user.id, permissions=permissions)
            await update.message.reply_text(f"🔇 {target_user.first_name} ကို စာရေးခွင့် (Mute) ပိတ်လိုက်ပါပြီ။")
        except TelegramError:
            await update.message.reply_text("❌ Bot မှာ Mute ဖို့ အခွင့်အာဏာ မရှိသေးပါဘူး။")
    else:
        await update.message.reply_text("❌ Mute ချင်တဲ့သူရဲ့စာကို Reply ပြန်ပြီး /mute လို့ ရိုက်ပေးပါ။")

async def mention_admins(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        admins = await context.bot.get_chat_administrators(update.effective_chat.id)
        admin_list = "📢 **Admin များ အရေးပေါ်ခေါ်နေပါတယ်ရှင့်-**\n"
        for admin in admins:
            if not admin.user.is_bot and admin.user.username:
                admin_list += f"@{admin.user.username} "
        await update.message.reply_text(admin_list, parse_mode="Markdown")
    except TelegramError:
        await update.message.reply_text("❌ Admin စာရင်းဆွဲထုတ်လို့ မရပါဘူးရှင်။")

# ================== MAIN APP ==================

def main():
    if not TOKEN:
        print("❌ Error: BOT_TOKEN ကို .env ဖိုင်ထဲမှာ ရှာမတွေ့ပါ။")
        return

    app = Application.builder().token(TOKEN).build()

    # Commands Linkings
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("boy", set_boy))
    app.add_handler(CommandHandler("girl", set_girl))
    app.add_handler(CommandHandler("love", match_love))
    app.add_handler(CommandHandler("ban", ban_user))
    app.add_handler(CommandHandler("mute", mute_user))
    app.add_handler(CommandHandler("admin", mention_admins))

    print("🚀 Bot စတင်ပွင့်သွားပါပြီ... လုံခြုံရေးစနစ် အပြည့်အဝ အလုပ်လုပ်နေပါပြီ။")
    app.run_polling()

if __name__ == '__main__':
    main()
    
