from whatsappy import whatsapp

whatsapp.login()

whatsapp.select_chat_by_name('Family Group')
if whatsapp.last_message() == "Leave":
    whatsapp.leave_group()  # <--

whatsapp.close()
