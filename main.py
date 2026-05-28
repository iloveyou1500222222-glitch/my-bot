import telebot
import os8738992752:AAEc0SDy-JjFfdB2U2pzcZfZAtg5iPNqSLQ
import threading

bot = telebot.TeleBot('8738992752:AAEc0SDy-JjFfdB2U2pzcZfZAtg5iPNqSLQ')
ADMIN_ID = 7771663458

@bot.message_handler(func=lambda m: True)
def save(m):
    cid = str(m.chat.id)
    if not os.path.exists("chats.txt"): open("chats.txt", "w").close()
    if cid not in open("chats.txt").read():
        with open("chats.txt", "a") as f: f.write(cid + "\n")

@bot.message_handler(commands=['broadcast'])
def bc(m):
    if m.from_user.id == ADMIN_ID:
        text = m.text.replace('/broadcast', '').strip()
        for cid in open("chats.txt").readlines():
            try: bot.send_message(cid.strip(), text)
            except: pass
        bot.reply_to(m, "ပို့ပြီးပါပြီ")

bot.infinity_polling()
