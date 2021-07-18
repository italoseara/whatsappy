from whatsappy import whatsapp

whatsapp.login()

whatsapp.select_chat_by_name('Family Group')
whatsapp.change_group_name('Family Group') # <--
whatsapp.close()