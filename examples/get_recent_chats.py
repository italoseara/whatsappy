from whatsappy import whatsapp

whatsapp.login()

recent_chats = whatsapp.get_pinned_chats() # <--
print(recent_chats)

whatsapp.exit()