import telebot
import random
import os

TOKEN = '8738992752:AAEc0SDy-JjFfdB2U2pzcZfZAtg5iPNqSLQ'
OWNER_IDS = [7771663458, 853383380]

bot = telebot.TeleBot(TOKEN)
love_db = {} # {user_id: partner_id}

# Admin/Owner စစ်ဆေးခြင်း
def is_owner(uid): return uid in OWNER_IDS

# 1. Welcome Message & Auto Join
@bot.message_handler(content_types=['new_chat_members'])
def welcome(message):
    for member in message.new_chat_members:
        bot.reply_to(message, f"ကြိုဆိုပါတယ်နော် မမသဲလေး😘 @{member.username or member.first_name}")

# 2. Dating System
@bot.message_handler(commands=['tloveboy', 'tloveဂား'])
def tlove(message):
    bot.reply_to(message, "ရည်းစားရှာပေးနေပါပြီ... ခဏစောင့်ပေးပါရှင့်!")

@bot.message_handler(commands=['love'])
def match_love(message):
    uid = message.from_user.id
    if uid in love_db:
        bot.reply_to(message, "သင်ချိတ်ဆက်ပြီးသားဖြစ်နေပါပြီ။")
    else:
        # ဒီနေရာမှာ ကျပန်းချိတ်ဆက်ပေးမယ့် logic ထည့်ရပါမယ်
        bot.reply_to(message, "အောင်မြင်စွာ ချိတ်ဆက်ပေးလိုက်ပါပြီ!")

@bot.message_handler(commands=['nolove'])
def no_love(message):
    uid = message.from_user.id
    if uid in love_db:
        del love_db[uid]
        bot.reply_to(message, "ချိတ်ဆက်ထားတာကို အောင်မြင်စွာ ဖျက်လိုက်ပါပြီ။")

# 3. Mute/Ban System
@bot.message_handler(commands=['ban', 'mute', 'umute', 'muteadmin', 'umuteadmin'])
def admin_commands(message):
    if not is_owner(message.from_user.id):
        bot.reply_to(message, "Admin/Owner များသာ သုံးနိုင်ပါသည်။")
        return
    
    cmd = message.text.split()[0]
    if cmd == '/ban':
        bot.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
        bot.reply_to(message, "ဘန်လိုက်ပါပြီ။")
    elif cmd == '/mute':
        bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, can_send_messages=False)
        bot.reply_to(message, "မြူးလိုက်ပါပြီ။")

# 4. Info Commands
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "မဂ်လာပာအသုံးပြုသူရှင့်😘။ Gpထဲbotလေးထည့်ပေးနော်။ အာဘွားသဲလေး🤪😍 /help ကိုနိပ်၍အသုံးပြုပုံကြည့်ပာရှင့်။ ကြောညာထဲလို့ပာက owner နတ်သားလေး @Tear808")

@bot.message_handler(commands=['help'])
def help_cmd(message):
    bot.reply_to(message, "အသုံးပြုပုံ - /love (ရည်းစားချိတ်), /nolove (ချိတ်ဖြုတ်), /ban, /mute, /botowner")

@bot.message_handler(commands=['botowner'])
def owner_cmd(message):
    bot.reply_to(message, "Bot ပိုင်ရှင်မှာ @Tear808 ဖြစ်ပါသည်။")

bot.infinity_polling()

