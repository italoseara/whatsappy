from whatsappy import whatsapp

whatsapp.login()

whatsapp.select_chat_by_name('Family Group')
while True:
    if whatsapp.new_message():
        if whatsapp.last_message() == "Good Morning!":
            whatsapp.reply("Good Morning!")  # <--

whatsapp.close()
