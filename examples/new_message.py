from whatsappy import whatsapp

whatsapp.login()

whatsapp.select_chat_by_name('Family Group')
while True:
    if whatsapp.new_message():  # <--
        whatsapp.send("Hello")

