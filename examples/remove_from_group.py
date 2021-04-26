from whatsappy import whatsapp

whatsapp.login()

whatsapp.select_chat("Family Group")
whatsapp.remove_from_group("Cousin")  # <--
whatsapp.close()
