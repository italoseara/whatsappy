from whatsappy import whatsapp

whatsapp.login()

whatsapp.select_chat('Family Group')
whatsapp.change_group_name('Happy Family') # <--
whatsapp.close()
