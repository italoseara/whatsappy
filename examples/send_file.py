from whatsappy.wpp import whatsapp

whatsapp.login()

whatsapp.select_chat('Family Group')
whatsapp.send_file('C://file.txt') # <--

whatsapp.exit()