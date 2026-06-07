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
def home(): return "မြနှင်း Bot Online & Fully Functional! ❤️"

def run():
    port = int(os.environ.get("PORT", 8080))
    app_flask.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run, daemon=True)
    t.start()

# --- Settings ---
TOKEN = os.environ.get("BOT_TOKEN") 
OWNER_ID = 7771663458  
registered_users = {} 
game_data = {}  
group_list = set()  

logging.basicConfig(level=logging.INFO)

# --- Security ---
async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    if update.effective_chat.type == "private": return False
    user_id = update.effective_user.id
    if user_id == OWNER_ID: return True
    try:
        member = await context.bot.get_chat_member(update.effective_chat.id, user_id)
        return member.status in ['administrator', 'creator']
    except: return False

# --- Welcome (အချွဲဆုံးစနစ်) ---
async def welcome_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        if member.id == context.bot.id: 
            group_list.add(update.effective_chat.id)
            await update.message.reply_text("🎀 မင်္ဂလာပါရှင့်... **မြနှင်း** ရောက်လာပါပြီ။ အားလုံးနဲ့ ရင်းနှီးချင်ပါတယ်နော်... အာဘွား! 😘💕")
            continue
        welcome_texts = [
            f"ဟယ်... အချောလေး @{member.username or member.first_name} ရေ... 🎀 **မြနှင်း** ရဲ့ ရင်ခွင်ထဲကို ကြိုဆိုပါတယ်ရှင့်။ 🥰💖",
            f"တကတည်း... ကြည့်ပါဦး၊ ဘယ်သူလေး ရောက်လာတာလဲ... @{member.username or member.first_name} လေး ကြိုဆိုပါတယ်နော်... မြနှင်းနဲ့ အတူတူ ဖူးစာရှာကြမယ်လေ... 😍✨",
            f"အသည်းကျော်လေး @{member.username or member.first_name} လေး ရောက်လာပြီ... 😘 ဒီ Group လေးထဲမှာ ပျော်ရွှင်ပါစေနော်... မြနှင်းက အမြဲစောင့်နေမှာပါ... 💋🌸"
        ]
        await update.message.reply_text(random.choice(welcome_texts), parse_mode='Markdown')

# --- Admin Call ---
async def call_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == "private": return
    try:
        admins = await context.bot.get_chat_administrators(update.effective_chat.id)
        mentions = [f"@{a.user.username}" for a in admins if a.user.username]
        if "@Tear808" not in mentions: mentions.append("@Tear808")
        await update.message.reply_text(f"📣📣 **Admin လေးတို့နဲ့ Owner လေးရေ... အကူအညီလိုနေလို့ပါရှင်** 🥰\n\n{' '.join(mentions)}")
    except: await update.message.reply_text("❌ Admin စာရင်းရယူလို့မရပါရှင့် (Bot ကို Admin ပေးထားပါဦး)။")

# --- Broadcast ---
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID: return
    if not update.message.reply_to_message:
        await update.message.reply_text("💡 ဖြန့်ချင်တဲ့ Post ကို Reply ပြန်ပြီး /bcast ရိုက်ပါရှင့်။")
        return
    total = len(group_list)
    success = 0
    status_msg = await update.message.reply_text(f"⏳ စတင်ပို့ဆောင်နေပါပြီ... (စုစုပေါင်း GP: {total} ခု)")
    for chat_id in list(group_list):
        try:
            await context.bot.copy_message(chat_id, update.effective_chat.id, update.message.reply_to_message.message_id)
            success += 1
        except: group_list.discard(chat_id)
    await status_msg.edit_text(f"✅ ပို့ဆောင်မှု ပြီးဆုံးပါပြီ! \n🎯 စုစုပေါင်း {total} ခုထဲမှ {success} ခုသို့ အောင်မြင်စွာ ပို့ပေးလိုက်ပါပြီ။ 🥰")

# --- Games ---
async def set_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cmd = update.message.text.lower()
    game = "MLBB 🎮" if "/mlbb" in cmd else "PUBG 🔫"
    game_data[update.effective_user.id] = game
    await update.message.reply_text(f"🎮 {game} ဂိမ်းကို သင့်ရဲ့ အဓိကဂိမ်းအဖြစ် သတ်မှတ်လိုက်ပါပြီရှင့်! 🥰🔥")

async def find_buddy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cmd = update.message.text.lower()
    target_game = "MLBB 🎮" if "/mbbfriend" in cmd else "PUBG 🔫"
    potential = [uid for uid, g in game_data.items() if g == target_game and uid != update.effective_user.id]
    if not potential: await update.message.reply_text(f"⏳ {target_game} ဆော့မယ့်သူ ရှာမတွေ့သေးဘူးရှင့်... 🥺💕"); return
    buddy = context.bot.get_chat_member(update.effective_chat.id, random.choice(potential)).user
    await update.message.reply_text(f"🎮 **Game Buddy တွေ့ပြီ!**\n👤 Player: @{buddy.username}\n✨ ID လဲလှယ်ပြီး ပျော်ပျော်ဆော့ကြပါရှင့်! 🥰💋")

# --- Commands ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type in ["group", "supergroup"]: group_list.add(update.effective_chat.id)
    await update.message.reply_text("မင်္ဂလာပါရှင့် 😘✨\n\n🎀 **မြနှင်း** 🎀 ကို Group ထဲထည့်ပေးလို့ ကျေးဇူးပါရှင်။\n👑 Owner ချောလေး - @Tear808\n\nအသုံးပြုပုံကြည့်ရန် - /help နှိပ်ပေးပါရှင့်။ 👇🥺👈")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = ("✨ *မြနှင်း Bot လမ်းညွှန်* ✨\n\n👤 /boy , /girl - စာရင်းသွင်း\n💖 /love - အတွဲချိတ်\n🎮 /mlbb , /pubg - ဂိမ်းသတ်မှတ်ရန်\n🎯 /mbbfriend , /pubgfriend - ဂိမ်းဖော်ရှာရန်\n📢 /admin - Admin ခေါ်ရန်\n\n🛡 *Admin Tools*\n🚫 /ban , 🤫 /mute , 🔊 /umute")
    await update.message.reply_text(msg, parse_mode='Markdown')

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id
    cmd = update.message.text.split()[0].lower()
    if not user.username: await update.message.reply_text("❌ Username အရင်ဆောက်ပေးပါဦးနော်..."); return
    gender = "Boy 👨" if "boy" in cmd else "Girl 👩"
    if chat_id not in registered_users: registered_users[chat_id] = {}
    registered_users[chat_id][user.id] = {"username": f"@{user.username}", "gender": gender}
    await update.message.reply_text(f"✨ {gender} အဖြစ် သတ်မှတ်ပြီးပါပြီ! 🥰")

async def love_match(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    if chat_id not in registered_users or user_id not in registered_users[chat_id]:
        await update.message.reply_text("🚨 အရင်ဆုံး /boy ဒါမှမဟုတ် /girl နဲ့ စာရင်းသွင်းပါဦးရှင့်။")
        return
    me = registered_users[chat_id][user_id]
    potential = [uid for uid, data in registered_users[chat_id].items() if uid != user_id and data["gender"] != me["gender"]]
    if not potential: await update.message.reply_text("⏳ ဖူးစာရှင်လေးတွေ ရှာမတွေ့သေးပါဘူး သဲလေး... 🥺💗"); return
    partner = registered_users[chat_id][random.choice(potential)]
    await update.message.reply_text(f"🎀 မြှားနတ်မောင်မြှားပစ်လိုက်ပါပီရှင့် 🎀\n\nအတွဲလေးကတော့ {me['username']} နဲ့ {partner['username']} တို့ပဲ ဖြစ်ပါတယ်ရှင့်! 🤪✨")

async def admin_tools(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context) or not update.message.reply_to_message: return
    target = update.message.reply_to_message.from_user
    cmd = update.message.text.split()[0].lower()
    try:
        if '/ban' in cmd: await context.bot.ban_chat_member(update.effective_chat.id, target.id); await update.message.reply_text(f"📣 ထွက်သွားလိုက်တော့နော် @{target.username} 🤬")
        elif '/mute' in cmd: await context.bot.restrict_chat_member(update.effective_chat.id, target.id, ChatPermissions(can_send_messages=False)); await update.message.reply_text(f"📣 ခဏလေးအသံတိတ်ပေးပါဦးနော် @{target.username} 😘")
        elif '/umute' in cmd: await context.bot.restrict_chat_member(update.effective_chat.id, target.id, ChatPermissions(can_send_messages=True)); await update.message.reply_text(f"📣 စကားပြန်ပြောလို့ရပီသဲယေး @{target.username} 😘")
    except: pass

def main():
    if not TOKEN: return
    keep_alive()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("bcast", broadcast))
    app.add_handler(CommandHandler(["boy", "girl"], register))
    app.add_handler(CommandHandler("love", love_match))
    app.add_handler(CommandHandler(["mlbb", "pubg"], set_game))
    app.add_handler(CommandHandler(["mbbfriend", "pubgfriend"], find_buddy))
    app.add_handler(CommandHandler(["ban", "mute", "umute"], admin_tools))
    app.add_handler(CommandHandler("admin", call_admin))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_member))
    app.add_handler(MessageHandler(filters.ChatType.GROUPS & ~filters.COMMAND, lambda u, c: group_list.add(u.effective_chat.id)))
    app.run_polling()

if __name__ == '__main__': main()
      
