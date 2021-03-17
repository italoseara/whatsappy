from whatsappy.wpp import whatsapp

whatsapp.login()

whatsapp.select_chat('Family Group')

while True:
    if whatsapp.new_message(): # <--
        whatsapp.send('Hello')

whatsapp.exit()