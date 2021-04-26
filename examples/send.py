from whatsappy import whatsapp

whatsapp.login()

whatsapp.select_chat("Family Group")
whatsapp.send("Hello")

whatsapp.close()
