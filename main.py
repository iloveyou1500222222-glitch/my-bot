import telebot
import random
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
/boy  -မြှားနတ်မောင်
/admin - Admin 🧑‍🤝‍🧑👭Ban ခေါ်ရန်
/ban - (Admin) Reply လုပ်ပြီး Ban 🚫🚫ရန််ပြီး
/mute - (Admin) Reply လုပ်ပြီး Mute 📵📵ရန််
/umute - (Admin) Reply လုပ်ပြီး Unmut❓ရန်
/girl -မိန်းခ‌ေလးအဖစ်စာရင်းဝင်ပီရှင့်💝
/boy -ယောက်ျားလေးအဖစ်စာရင်းဝင်ပီရှင့်💝"""
#---------------------------------------------------------

bot = telebot.TeleBot(TOKEN)
user_pool = [] 
# ၁။ Start လုပ်မှ ကြော်ငြာနှင့် ဝယ်ကမ်း msg ပေါ်ခြင်း
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, f"{WELCOME_MSG}\n\n{AD_TEXT}")

# ၂။ @bot.message_handler(commands=['boy'])
def set_boy(message):
    boys.append({'id': message.from_user.id, 'name': message.from_user.first_name, 'username': message.from_user.username})
    bot.reply_to(message, "✅ သင် ယောကျာ်းလေးအဖြစ် စာရင်းသွင်းပြီးပါပြီ💝✅။" + AD_TEXT)

@bot.message_handler(commands=['girl'])
def set_girl(message):
    girls.append({'id': message.from_user.id, 'name': message.from_user.first_name, 'username': message.from_user.username})
    bot.reply_to(message, "✅ သင် မိန်းကလေးအဖြစ် စာရင်းသွင်းပြီးပါပြီ💝✅။" + AD_TEXT)

@bot.message_handler(commands=['love'])
def match(message):
    if boys and girls:
        b = boys.pop(0)
        g = girls.pop(0)
        # @username နဲ့ ခေါ်ပေးခြင်း
        b_mention = f"@{b['username']}" if b['username'] else b['name']
        g_mention = f"@{g['username']}" if g['username'] else g['name']
        
        bot.send_message(message.chat.id, f"🎉 မြှားနတ်မောင်မြှားပစ်လိုက်ပီ✅✅! {b_mention} နှင့် {g_mention} တို့ အတွဲများ ဖြစ်သွားပါပီရှင့်။ 💖{AD_TEXT}")
    else:
        bot.reply_to(message, "⚠️ စာရင်းထဲတွင် တွဲရန် လူမလုံလောက်သေးပါ။ /boy သို့မဟုတ် /girl နဲ့ စာရင်းသွင်းပေးပါဦးအာဘွား‌ေပးမယ်။" + AD_TEXT)
@bot.message_handler(commands=['admin'])
def call_admin(message):
    mentions = " ".join([f"[Admin](tg://user?id={uid})" for uid in OWNER_IDS])
    bot.reply_to(message, f"📢 Admin $message Admin$ချောများရှင့်💝💝! အကူအညီ လိုအပ်နေပါတယ်gpလာခဲ့အုန်းမလာရင်စော်ပစ်။ဘဲပစ်မဖစ်ပစေတော်🤪😒 - {mentions}\n\n{AD_TEXT}", parse_mode="Markdown")

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
            bot.reply_to(message, "🔊 စကားပြောခွင့် ပြန်ပေးလိုကပြန်ပေးလိုက်ပါပြရှင့်သဲ‌ယေး။")
            import telebot

# Bot ရောက်နေတဲ့ Group ID တွေကို သိမ်းထားမယ့် စာရင်း
groups = set()

def is_owner(uid): return uid in OWNER_IDS

@bot.message_handler(commands=['broadcast'])
def broadcast(message):
    if not is_owner(message.from_user.id): return
    # /broadcast လို့ရိုက်ပြီး နောက်ကစာကို ပို့ပေးမယ်
    ad_content = message.text.replace('/broadcast ', '')
    if ad_content == '/broadcast':
        bot.reply_to(message, "ကြော်ငြာစာသား ထည့်ပေးပါဦး Admin ကြီး!")
        return
    
    for gid in groups:
        try:
            bot.send_message(gid, ad_content)
        except: continue
    bot.reply_to(message, "✅ ကြော်ငြာများ ပို့ပြီးပါပြီ!")

@bot.message_handler(commands=['start'])
def start(message):
    groups.add(message.chat.id) # Group ID ကို မှတ်ထားမယ်
    bot.reply_to(message, "မင်္ဂလာပါ! Bot လေး အဆင်သင့်ဖြစ်ပါပြီ။")

# ... ကျန်တဲ့ code တွေကို အရင်အတိုင်း ထားပါ ...
bot.infinity_polling()
