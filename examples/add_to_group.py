from whatsappy import whatsapp

whatsapp.login()

whatsapp.select_chat_by_name('Family Group')
whatsapp.add_to_group('Mom') # <--
whatsapp.close()