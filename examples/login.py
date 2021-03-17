from whatsappy.wpp import whatsapp

whatsapp.login(visible=False) # <-- Make it True if you want to see the process

whatsapp.select_chat('Family Group')
whatsapp.send('Good Morning!')
whatsapp.exit()