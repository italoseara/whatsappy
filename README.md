# Whatsappy

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://pepy.tech/badge/whatsappy-py)](https://pepy.tech/project/whatsappy-py)

## Overview

Whatsappy is a Python library for interacting with WhatsApp Web using Selenium. With this library, you can automate WhatsApp tasks such as sending messages, creating groups, and more.

## Requirements

- Python 3.11+
- Selenium
- Pillow
- Webdriver Manager
- QRCode

## Installation

You can install Whatsappy using pip:

```bash
pip install my-library-name
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

- `driver: (webdriver.Chrome)`: The Chrome driver.
- `unread_messages: (List[Unread])`: List of unread messages.

#### Methods

- `run()`: Opens WhatsApp Web in Chrome.
- `close()`: Closes the Chrome window.
- `open(chat: str) -> (Chat | Group | None)`: Selects a chat by name and returns a `Chat` or `Group` instance. Returns `None` if the chat does not exist.

### Chat

#### Properties

- `name: str`: The name of the chat.
- `number: str`: The number of the chat.
- `about: str`: The about of the chat.
- `profile_picture: JpegImageFile`: The profile picture of the chat.
- `starred_messages: List[str]`: The starred messages of the chat.


#### Methods

- `send(message: str, attachments: Optional[List[str]] = None)`: Sends a message to the chat.

### Group

#### Properties

- `subject: str`: The subject of the group.
- `description: str`: The description of the group.
- `profile_picture: Optional[JpegImageFile]`: The profile picture of the group.
- `participants: List[str]`: The participants of the group.
- `starred_messages: List[str]`: The starred messages of the group.

#### Methods

- `send(message: str, attachments: Optional[List[str]] = None)`: Sends a message to the group.

### Unread

#### Properties

- `name: str`: The name of the chat.
- `count: int`: The number of unread messages in the chat.
- `message: Optional[str]`: The last message in the chat.

#### Methods

- `reply(message: str, attachments: Optional[List[str]] = None)`: Replies to the unread chat with a message.

## License

# link to mit license file
Whatsappy is licensed under the [MIT License](LICENSE)