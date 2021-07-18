from whatsappy import whatsapp

whatsapp.login()

whatsapp.select_chat_by_name('Family Group')
invite_link = whatsapp.get_group_invite_link() # <--

whatsapp.close()