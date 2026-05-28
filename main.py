import telebot

# --- Settings ---
TOKEN = '8738992752:AAEc0SDy-JjFfdB2U2pzcZfZAtg5iPNqSLQ'
OWNER_IDS = [7771663458, 853383380]
AD_TEXT = "\n\n━━━━━━━━━━━━━━\n📢 ကြော်ငြာ - Bot ပိုင်ရှင် နတ်သားလေး @Tear808 ဆီသို့ ဆက်သွယ်နိုင်ပါသည်ရှင့်။ 👑"

bot = telebot.TeleBot(TOKEN)
boys, girls = [], []

def safe_send(chat_id, text):
    bot.send_message(chat_id, text + AD_TEXT)

# --- Commands ---
@bot.message_handler(commands=['start'])
def start(message):
    safe_send(message.chat.id, "မင်္ဂလာပါ! Bot လေး အဆင်သင့်ဖြစ်ပါပြီ။ /help တွင် အသုံးပြုပုံ ကြည့်ပါ။")

@bot.message_handler(commands=['help'])
def help_cmd(message):
    help_text = (
        "✨ *Bot အသုံးပြုပုံ* ✨\n\n"
        "/boy - ယောကျာ်းလေးအဖြစ် စာရင်းသွင်းရန် 🏃‍♂️\n"
        "/girl - မိန်းကလေးအဖြစ် စာရင်းသွင်းရန် 🏃‍♀️\n"
        "/love - တွဲရန် (၂ ယောက်ပြည့်လျှင် တွဲပေးမည်) 💖\n"
        "/admin - Admin များအား ခေါ်ရန် 📢\n"
        "/ban - (Admin) Reply လုပ်ပြီး Ban ရန် 🚫\n"
        "/mute - (Admin) Reply လုပ်ပြီး Mute ရန် 🤫\n"
        "/umute - (Admin) Reply လုပ်ပြီး Unmute ရန် 🔊"
    )
    safe_send(message.chat.id, help_text)

@bot.message_handler(commands=['boy'])
def set_boy(message):
    boys.append({'id': message.from_user.id, 'name': message.from_user.first_name, 'username': message.from_user.username})
    safe_send(message.chat.id, "✅ သင် ယောကျာ်းလေးအဖြစ် စာရင်းသွင်းပြီးပါပြီ။💖✅")

@bot.message_handler(commands=['girl'])
def set_girl(message):
    girls.append({'id': message.from_user.id, 'name': message.from_user.first_name, 'username': message.from_user.username})
    safe_send(message.chat.id, "✅ သင် မိန်းကလေးအဖြစ် စာရင်းသွင်းပြီးပါပြီ။💖✅")

@bot.message_handler(commands=['love'])
def match(message):
    if boys and girls:
        b = boys.pop(0)
        g = girls.pop(0)
        b_mention = f"@{b['username']}" if b['username'] else b['name']
        g_mention = f"@{g['username']}" if g['username'] else g['name']
        safe_send(message.chat.id, f"🎉 မြှားနတ်မောင်မြှားပစ်လိုက်ပီ! {b_mention} နှင့် {g_mention} တို့ အတွဲများ ဖြစ်သွားပါမြှားပစ်ခံကလို့ခိခိ။ 💖✅")
    else:
        safe_send(message.chat.id, "⚠️ တွဲရန် လူမလုံလောက်သေးပါ။ /boy သို့မဟုတ် /girl နဲ့ စာရင်းသွင်းပေးပါ။")

@bot.message_handler(commands=['admin'])
def call_admin(message):
    mentions = " ".join([f"[Admin](tg://user?id={uid})" for uid in OWNER_IDS])
    safe_send(message.chat.id, f"📢 Admin များရှင့်! အကူအညီ လိုအပ်နေပါတယ် - {mentions}")

@bot.message_handler(commands=['ban', 'mute', 'umute'])
def admin_tools(message):
    if message.from_user.id not in OWNER_IDS: return
    if not message.reply_to_message:
        safe_send(message.chat.id, "⚠️ ကျေးဇူးပြု၍ သူတစ်ယောက်ယောက်၏ Message ကို Reply လုပ်ပြီး ရိုက်ပေးပါ။")
        return
    
    target = message.reply_to_message.from_user.id
    try:
        if message.text == '/ban':
            bot.ban_chat_member(message.chat.id, target)
            safe_send(message.chat.id, "🚫 Ban လိုက်ပါပြီ အကျင့်မကောင်းတဲ့သူသွားတော့ group ကနေ 😡😡")
        elif message.text == '/mute':
            bot.restrict_chat_member(message.chat.id, target, can_send_messages=False)
            safe_send(message.chat.id, "🤫 Mute လိုက်ပါပြီ စိတ်ဆိုးတယ် 😡")
        elif message.text == '/umute':
            bot.restrict_chat_member(message.chat.id, target, can_send_messages=True)
            safe_send(message.chat.id, "🔊 စကားပြောခွင့် ပြန်ပေးလိုက်ပါပြီ ပြန်ပြောလို့ရပါပြီ 🗣")
    except Exception as e:
        safe_send(message.chat.id, "⚠️ Error: Bot ကို Group ထဲမှာ Admin အရင်ပေးထားပါဦး (Ban/Mute အမှန်ခြစ် ပေးထားပါ)။")

bot.infinity_polling()
