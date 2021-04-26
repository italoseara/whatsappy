from whatsappy import whatsapp

whatsapp.login()

whatsapp.select_chat("Family Group")
whatsapp.send("Good Morning!")
whatsapp.close()  # <--
