from whatsappy import whatsapp

whatsapp.login()

whatsapp.select_chat_by_name('Family Group')
whatsapp.make_group_admin('Dad') # <--
whatsapp.close()
