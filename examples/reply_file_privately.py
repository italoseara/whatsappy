from whatsappy import whatsapp

whatsapp.login()

whatsapp.select_chat_by_name('Family Group')

while True:
    if whatsapp.new_message():
        if whatsapp.last_message() == '!screenshot':
            whatsapp.reply_privately('C:/screenshot.png') # <--

whatsapp.close()