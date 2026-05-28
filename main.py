import telebot

TOKEN = '8738992752:AAEc0SDy-JjFfdB2U2pzcZfZAtg5iPNqSLQ'
OWNER_IDS = [7771663458, 853383380]

bot = telebot.TeleBot(TOKEN)
boys, girls = [], []

# ကြော်ငြာစာတန်း (ဒီနေရာမှာ ပြင်ချင်တာ ပြင်လို့ရပါတယ်)
AD = "\n\n━━━━━━━━━━━━━━\n📢 ကြော်ငြာ - Bot ပိုင်ရှင် နတ်သားလေး @Tear808 ဆီသို့ ဆက်သွယ်နိုင်ပါသည်ရှင့်။ 👑"

def is_owner(uid): return uid in OWNER_IDS

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "မင်္ဂလာပါ အသုံးပြုသူရှင့်!😘 Gp ထဲ bot လေး ထည့်ပေးနော်။ အာဘွားသဲလေး🤪😍 /help ကိုနှိပ်၍ အသုံးပြုပုံကြည့်ပါရှင့်။" + AD)

@bot.message_handler(commands=['help'])
def help_cmd(message):
    help_text = ("✨ *Bot အသုံးပြုပုံ* ✨\n/love - တွဲရန်\n/boy - ယောကျာ်းလေးအဖြစ် မှတ်ပုံတင်ရန်\n/girl - မိန်းကလေးအဖြစ် မှတ်ပုံတင်ရန်\n/admin - Admin ခေါ်ရန်\n/ban - (Admin) Reply လုပ်ပြီး Ban ရန်\n/mute - (Admin) Reply လုပ်ပြီး Mute ရန်\n/umute - (Admin) Reply လုပ်ပြီး Unmute ရန်" + AD)
    bot.reply_to(message, help_text, parse_mode="Markdown")

@bot.message_handler(commands=['boy', 'girl'])
def register(message):
    uid = {'id': message.from_user.id, 'name': message.from_user.first_name}
    if message.text == '/boy': boys.append(uid)
    else: girls.append(uid)
    
    if boys and girls:
        b, g = boys.pop(0), girls.pop(0)
        bot.send_message(message.chat.id, f"🎉 *{b['name']}* နှင့် *{g['name']}* တို့ အတွဲများဖြစ်သွားပါပြီ! 💖" + AD)
    else:
        bot.reply_to(message, "စာရင်းသွင်းပြီးပါပြီ။ နောက်တစ်ယောက်ကို စောင့်ပေးပါရှင့်! 🌸" + AD)

@bot.message_handler(commands=['ban', 'mute', 'umute', 'admin', 'botowner'])
def admin_cmd(message):
    cmd = message.text.split()[0]
    if cmd == '/admin':
        bot.reply_to(message, "📢 Admin များရှင့်! အကူအညီလိုနေပါသည်ရှင့်😭။ 🆘" + AD)
    elif cmd == '/botowner':
        bot.reply_to(message, "Bot ပိုင်ရှင်မှာ @Tear808 နတ်သားလေးဖြစ်ပါသည်။ 👑" + AD)
    elif is_owner(message.from_user.id) and message.reply_to_message:
        target = message.reply_to_message.from_user.id
        if cmd == '/ban':
            bot.ban_chat_member(message.chat.id, target)
            bot.reply_to(message, "🚫 Ban လိုက်ပါပြီ။" + AD)
        elif cmd == '/mute':
            bot.restrict_chat_member(message.chat.id, target, can_send_messages=False)
            bot.reply_to(message, "🤫 Mute လိုက်ပါပြီ။" + AD)
        elif cmd == '/umute':
            bot.restrict_chat_member(message.chat.id, target, can_send_messages=True)
            bot.reply_to(message, "🔊 စကားပြောခွင့် ပြန်ပေးလိုက်ပါပြီ။" + AD)

@bot.message_handler(content_types=['new_chat_members'])
def welcome(message):
    for member in message.new_chat_members:
        bot.reply_to(message, f"ကြိုဆိုပါတယ်နော် မမသဲလေး😘 @{member.username or member.first_name} အာဘွားသဲလေး🤪😍" + AD)

Group = telebot.TeleBot(TOKEN)
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
