from whatsappy import whatsapp

whatsapp.login()

whatsapp.select_chat_by_name('Family Group')
whatsapp.send_file('C://file.txt') # <--
whatsapp.close()
