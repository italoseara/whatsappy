# Whatsappy 4.0.0

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://pepy.tech/badge/whatsappy-py)](https://pepy.tech/project/whatsappy-py)

## Overview

Whatsappy is a Python library for interacting with WhatsApp Web using Selenium. With this library, you can automate WhatsApp tasks such as sending messages, creating groups, and more.

## Requirements

- Python 3.11+
- Chrome 94+

## Installation

You can install Whatsappy using pip:

```bash
pip install whatsappy-py
```

## Usage

Here's an example of how you can use Whatsappy to send a message:

```python
from whatsappy import Whatsapp

# Create a new instance of Whatsapp
whatsapp = Whatsapp()

# Create event handlers
@whatsapp.event
def on_ready():
    print("WhatsApp Web is ready!")

@whatsapp.event
def on_message(chat):
    print(f"New message from {chat.name}: {chat.message}")

# Open WhatsApp Web in Chrome
whatsapp.run()

# Select the chat you want to send a message to
chat = whatsapp.open("John Smith")

# Send a message
chat.send("Hello, John!")

# Close WhatsApp Web
whatsapp.close()
```

## API Reference

### Whatsapp

#### Properties

- `driver: webdriver.Chrome`: The Chrome driver.
- `unread_messages: List[UnreadMessage]`: List of unread messages.
- `me: Me`: The current user.
- `current_chat: str | None`: The name of the current chat. Returns `None` if no chat is selected.

#### Methods

- `run()`: Opens WhatsApp Web in Chrome.
- `close()`: Closes the Chrome window.
- `open(chat: str) -> (Chat | Group | None)`: Selects a chat by name and returns a `Chat` or `Group` instance. Returns `None` if the chat does not exist.

### Me

#### Properties

- `name: str`: The name of the user.
- `about: str`: The about of the user.
- `profile_picture: JpegImageFile`: The profile picture of the user.

### Chat

#### Properties

- `name: str`: The name of the chat.
- `number: str`: The number of the chat.
- `about: str`: The about of the chat.
- `profile_picture: JpegImageFile`: The profile picture of the chat.
- `last_message: Message | None`: The last message of the chat.
- `is_muted: bool`: Whether the chat is muted or not.
- `is_blocked: bool`: Whether the chat is blocked or not.
- `is_pinned: bool`: Whether the chat is pinned or not.

#### Methods

- `send(message: str, attachments: Optional[List[str]] = None, type: Optional[str] = "auto")`: Sends a message to the chat.
- `mute()`: Mutes the chat.
- `unmute()`: Unmutes the chat.
- `block()`: Blocks the chat.
- `unblock()`: Unblocks the chat.
- `clear(keep_starred: bool = False)`: Clears the chat messages.
- `delete()`: Deletes the chat.
- `pin()`: Pins the chat.
- `unpin()`: Unpins the chat.

### Group

#### Properties

- `subject: str`: The subject of the group.
- `description: str`: The description of the group.
- `profile_picture: Optional[JpegImageFile]`: The profile picture of the group.
- `participants: int`: The number of participants of the group.
- `last_message: Message | None`: The last message of the group.
- `is_muted: bool`: Whether the group is muted or not.
- `is_pinned: bool`: Whether the group is pinned or not.

#### Methods

- `send(message: str, attachments: Optional[List[str]] = None, type: Optional[str] = "auto")`: Sends a message to the group.
- `mute()`: Mutes the group.
- `unmute()`: Unmutes the group.
- `leave()`: Leaves the group.
- `clear(keep_starred: bool = False)`: Clears the group messages.
- `pin()`: Pins the group.
- `unpin()`: Unpins the group.

### Message

#### Properties

- `chat: Chat | Group`: The chat the message belongs to.
- `author: str`: The author of the message.
- `content: str`: The content of the message.
- `timestamp: datetime.datetime`: The timestamp of the message.
- `attachments: List[str]`: The attachments of the message.
- `is_forwarded: bool`: Whether the message is forwarded or not.
- `is_reply: bool`: Whether the message is a reply or not.

#### Methods

- `reply(message: str, attachments: Optional[List[str]] = None, type: Optional[str] = "auto")`: Replies to the message.

### UnreadMessage

#### Properties

- `name: str`: The name of the chat.
- `count: int`: The number of unread messages in the chat.
- `message: Optional[str]`: The last message in the chat.

#### Methods

- `reply(message: str, attachments: Optional[List[str]] = None, type: Optional[str] = "auto")`: Replies to the unread chat with a message. and returns a `Chat` or `Group` instance.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

Whatsappy is licensed under the [MIT License](LICENSE)
