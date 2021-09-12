from whatsappy import whatsapp

whatsapp.login(visible=True)  # <-- Make it False if you don't want to see the process

whatsapp.select_chat('Family Group')
whatsapp.send('Good Morning!')
whatsapp.close()
