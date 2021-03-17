from whatsappy.wpp import whatsapp

whatsapp.login()

whatsapp.select_chat('Family Group')
whatsapp.send('Good Morning!')
whatsapp.exit() # <--