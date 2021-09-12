from whatsappy import whatsapp

whatsapp.login()


# =====================================================

# By Name
whatsapp.select_chat("Family Group")  # <--

# =====================================================

# By Number
whatsapp.send("00180808080")  # <--

# =====================================================

whatsapp.close()
