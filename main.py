import telebot
import random

# --- [အောက်ပါ Settings များကို စိတ်ကြိုက် ပြင်နိုင်ပါသည်] ---
TOKEN = '8738992752:AAEc0SDy-JjFfdB2U2pzcZfZAtg5iPNqSLQ'
OWNER_IDS = [7771663458, 853383380] # Admin IDs များ
AD_TEXT = "📢 ကြော်ငြာ - Bot ပိုင်ရှင် နတ်သားလေး @Tear808 ဆီသို့ ဆက်သွယ်နိုင်ပါသည်ရှင့်။ 🆘 👑"
WELCOME_MSG = "မင်္ဂလာပါရှင့်😘 ကျေးဇူးပြု၍ Group ထဲထည့်ပေးနော်သဲလေးအာဘွား။များရီချစ်တယ်😍😍"
# --------------------------------------------------------

bot = telebot.TeleBot(TOKEN)
user_pool = [] 
# Help စာသားကို ဒီနေရာမှာပဲ သီးသန့် ပြင်ပါ
HELP_MSG = """
✨ *Bot အသုံးပြုပုံ* ✨

/start - Bot စတင်ရန်
/help - အသုံးပြုပုံကြည့်ရန်
/love - တွဲရန် စာရင်းသွင်းမည်
/admin - Admin 🧑‍🤝‍🧑👭Ban ခေါ်ရန်
/ban - (Admin) Reply လုပ်ပြီး Ban 🚫🚫ရန််ပြီး
/mute - (Admin) Reply လုပ်ပြီး Mute 📵📵ရန််
/umute - (Admin) Reply လုပ်ပြီး Unmut❓ရန်
"""
# --------------------------------------------------------

bot = telebot.TeleBot(TOKEN)
user_pool = [] 
# ၁။ Start လုပ်မှ ကြော်ငြာနှင့် ဝယ်ကမ်း msg ပေါ်ခြင်း
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, f"{WELCOME_MSG}\n\n{AD_TEXT}")

# ၂။ /love ရိုက်မှ တွဲပေးခြင်း
@bot.message_handler(commands=['love'])
def love_match(message):
    uid = message.from_user.id
    name = message.from_user.first_name
    if {'id': uid, 'name': name} not in user_pool:
        user_pool.append({'id': uid, 'name': name})
        bot.reply_to(message, f"✅ {name} ရေ၊ ❤️‍🩹ရည်းစားရှာရန်စာရင်းထဲ ဝင်သွားပါပြီရှင့်🎉🎉။")
    
    if len(user_pool) >= 2:
        u1 = user_pool.pop(0)
        u2 = user_pool.pop(0)
        bot.send_message(message.chat.id, f"🎉 မြှားနတ်မောင်မြှားပစ်လိုက်ပီနော်! {u1['name']} နှင့် {u2['name']} တို့ အတွဲများ ဖြစ်သွားပါပြီသာယာတဲဘဝ‌ေလးဖြစ်‌ေစကွာ😊😘။ 💖\n\n{AD_TEXT}")

# ၃။ Admin အားလုံးကို Tag လုပ်ခေါ်ခြင်း
@bot.message_handler(commands=['admin'])
def call_admin(message):
    mentions = " ".join([f"[Admin](tg://user?id={uid})" for uid in OWNER_IDS])
    bot.reply_to(message, f"📢 Admin $ချောမျရှင့်! အကူအညီ လိုအပ်နေပါတယ်gpလာခဲ့အုန်းမလာရင်စော်ပစ်။ဘဲပစ်မဖစ်ပစေတော်🤪😒 - {mentions}\n\n{AD_TEXT}", parse_mode="Markdown")

# ၄။ Admin သီးသန့် အလုပ်များ
@bot.message_handler(commands=['ban', 'mute', 'umute'])
def admin_tools(message):
    if message.from_user.id not in OWNER_IDS: return
    if not message.reply_to_message: return
    
    target = message.reply_to_message.from_user.id
    try:
        if message.text == '/ban':
            bot.ban_chat_member(message.chat.id, target)
            bot.reply_to(message, "🚫 Ban လိုက်ပါပြီအကျင်မကောင်းတဲသူသွားငာgroup က။🤬🤬")
        elif message.text == '/mute':
            bot.restrict_chat_member(message.chat.id, target, can_send_messages=False)
            bot.reply_to(message, "🤫 Mute လိုက်ပါပြီစိတ်ဆိုးတယ်။")
        elif message.text == '/umute':
            bot.restrict_chat_member(message.chat.id, target, can_send_messages=True)
            bot.reply_to(message, "🔊 စကားပြောခွင့် ပြန်ပေးလိုက်ပါပြီရှင့်သဲ‌ေယး😘။")
 r
