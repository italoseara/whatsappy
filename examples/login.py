from whatsappy import whatsapp

whatsapp.login(visible=False)  # <-- Make it True if you want to see the process

whatsapp.select_chat_by_name('Family Group')
whatsapp.send('Good Morning!')
whatsapp.close()
