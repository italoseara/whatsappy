from whatsappy.wpp import whatsapp

whatsapp.login()

whatsapp.select_chat('Family Group')

if whatsapp.last_message() == 'Leave':
    whatsapp.leave_group() # <--

whatsapp.exit()