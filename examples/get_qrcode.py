from whatsappy import whatsapp

whatsapp.get_qrcode() # <--
whatsapp.login()

whatsapp.select_chat('Family Group')
whatsapp.send('Good Afternoon!')
whatsapp.close()