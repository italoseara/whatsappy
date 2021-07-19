from whatsappy import whatsapp

whatsapp.login()

whatsapp.select_chat_by_name('Family Group')
whatsapp.remove_from_group('Cousin') # <--
whatsapp.close()
