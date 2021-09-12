from whatsappy import whatsapp

whatsapp.login()

whatsapp.select_chat("Family Group")

message = whatsapp.last_message() # <--

# =====================================================

# General Properties and Functions

# =====================================================

# Text Property
if message.text == "Ping":
    message.reply("Pong")

# =====================================================

# Author Property
if message.author == "Mom":
    message.reply("Hi Mom!")

# =====================================================

# Quote Property
if message.quote.author == "You":
    message.reply_privately(f"You quoted me ({message.quote.text})")

# =====================================================

# Time Property
from datetime import time

sleep_time = time(21, 00) # 9:00 PM
if message.time.time() >= sleep_time:
    message.reply("Time to go to bed!")

# =====================================================

# Forwarded Property
if message.forwarded:
    message.reply("Your message was forwarded")

# =====================================================

# Forward Function
message.forward(contacts=["Mom", "Dad", "Cousin"])

# =====================================================

# Reply Function
if message.text == "Ping":
    message.reply("Pong")

# =====================================================

# Reply Privatly Function
if message.quote.author == "You":
    message.reply_privately(f"You quoted me ({message.quote.text})")

# =====================================================

# Delete Function
if message.text == "Delete me":
    message.delete()

# =====================================================

# Star Function
if message.text == "Star me":
    message.star()

# =====================================================

# Specific Properties and Functions

# =====================================================

# Document

print(message.file.type)
print(message.file.size)

with open(message.file.name, "wb+") as file:
    file.write(message.file.content)

# =====================================================

# Video

print(message.length)

# =====================================================

# Audio

print(message.isrecorded)
print(message.file.length)
print(message.file.size)

with open("audio.oga", "wb+") as file:
    file.write(message.file.content)

# =====================================================

# Image / Sticker

print(message.file.size)
print(message.file.resolution)

with open("photo.jpeg", "wb+") as file:
    file.write(message.file.content)

# =====================================================

# Contact Card

for contact in message.contacts:
    print(contact.name)
    print(contact.numbers)

# =====================================================

# Location / Live Location

print(message.coords)
print(message.link)
print(message.until) # Exclusive for Live Location

# =====================================================

whatsapp.close()