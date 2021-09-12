from whatsappy import whatsapp

whatsapp.login()

whatsapp.select_chat('Family Group')

if whatsapp.last_message().text == "Leave":
    whatsapp.leave_group()  # <--

whatsapp.close()
