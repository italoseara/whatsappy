from whatsappy import whatsapp

whatsapp.login()

whatsapp.select_chat_by_name("Family Group")
whatsapp.change_group_pfp("C:/picture.png") # <--
whatsapp.close()