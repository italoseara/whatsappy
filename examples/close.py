from whatsappy import whatsapp

whatsapp.login()

whatsapp.select_chat_by_name('Family Group')
whatsapp.send('Good Morning!')
whatsapp.close() # <--
