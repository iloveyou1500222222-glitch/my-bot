async def welcome_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # လူသစ်ဝင်လာတိုင်း Log ထဲမှာ ပြအောင်လုပ်မယ် (စစ်ဆေးဖို့)
    print(f"New member detected in chat {update.effective_chat.id}")
    
    for member in update.message.new_chat_members:
        if member.id == context.bot.id:
            continue
            
        welcome_msg = f"✨ မင်္ဂလာပါ သဲလေး @{member.username or member.first_name} ✨\n\nလာ... အခန်းထဲလာ 🥰💋"
        
        try:
            # ဗီဒီယိုအရင်ပို့မယ်
            await context.bot.send_video(
                chat_id=update.effective_chat.id,
                video=WELCOME_VIDEO,
                caption=welcome_msg,
                parse_mode='Markdown'
            )
        except Exception as e:
            # ဗီဒီယိုပို့မရရင် စာပဲပို့မယ်
            print(f"Video Error: {e}")
            await update.message.reply_text(welcome_msg)
          
