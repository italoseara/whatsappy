from whatsappy import whatsapp

whatsapp.login()

whatsapp.select_chat_by_number(14078888888) # <--
whatsapp.send('Hello')

whatsapp.close()