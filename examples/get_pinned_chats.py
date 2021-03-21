from whatsappy import whatsapp

whatsapp.login()

pinned_chats = whatsapp.get_pinned_chats() # <--
print(pinned_chats)

whatsapp.close()