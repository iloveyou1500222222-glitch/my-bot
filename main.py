import telebot
import time

TOKEN = '8738992752:AAEc0SDy-JjFfdB2U2pzcZfZAtg5iPNqSLQ'
OWNER_IDS = [7771663458, 853383380]

bot = telebot.TeleBot(TOKEN)
boys, girls = [], []

def is_owner(uid): return uid in OWNER_IDS

# Mute အချိန်အတွက်
def get_seconds(time_str):
    try:
        unit = time_str[-1]
        value = int(time_str[:-1])
        if unit == 's': return value
        if unit == 'm': return value * 60
        if unit == 'h': return value * 3600
    except: return 60
    return 60

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "မင်္ဂလာပါ! အသုံးပြုသူရှင့်😘။ /help ကိုနှိပ်၍ အသုံးပြုပုံ ကြည့်နိုင်ပါသည်။")

@bot.message_handler(content_types=['new_chat_members'])
def welcome(message):
    for member in message.new_chat_members:
        bot.reply_to(message, f"ကြိုဆိုပါတယ်နော် မမသဲလေး😘 @{member.username or member.first_name}")

@bot.message_handler(commands=['boy', 'girl'])
def dating_system(message):
    uid = {'id': message.from_user.id, 'name': message.from_user.first_name}
    if message.text == '/boy': boys.append(uid)
    else: girls.append(uid)
    
    if boys and girls:
        b, g = boys.pop(0), girls.pop(0)
        bot.send_message(message.chat.id, f"🎉 ဟိတ်မောင်၊ {b['name']} နှင့် {g['name']} တို့သည် ယနေ့မှစ၍ အတွဲများ ဖြစ်သွားပါပြီ။ 💖")
    else:
        bot.reply_to(message, "စာရင်းထဲ ထည့်ပေးလိုက်ပါပြီ။ နောက်တစ်ယောက်ကို စောင့်ပေးပါရှင့်! 🌸")

@bot.message_handler(commands=['mute'])
def mute_member(message):
    if not is_owner(message.from_user.id): return
    if message.reply_to_message:
        target = message.reply_to_message.from_user.id
        args = message.text.split()
        duration = get_seconds(args[1]) if len(args) > 1 else 60
        bot.restrict_chat_member(message.chat.id, target, until_date=time.time() + duration, can_send_messages=False)
        bot.reply_to(message, f"🤫 {duration} စက္ကန့်ကြာအောင် Mute လိုက်ပါပြီ။")

@bot.message_handler(commands=['umute'])
def unmute_member(message):
    if not is_owner(message.from_user.id): return
    if message.reply_to_message:
        bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, can_send_messages=True)
        bot.reply_to(message, "🔊 အချိန်မပြည့်ခင် စကားပြောခွင့် ပြန်ပေးလိုက်ပါပြီ။")

@bot.message_handler(commands=['ban'])
def ban_member(message):
    if not is_owner(message.from_user.id): return
    if message.reply_to_message:
        bot.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
        bot.reply_to(message, "🚫 အောင်မြင်စွာ Ban လိုက်ပါပြီ။")

@bot.message_handler(commands=['admin'])
def call_admin(message):
    bot.reply_to(message, "📢 Group Admin များအားလုံးကို ခေါ်လိုက်ပါပြီ!")

bot.infinity_polling()
        
