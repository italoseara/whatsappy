# whatsappy

Whatsappy is a Python library for creating whatsapp bots.

Creator: [Italo Seara](https://github.com/italoseara)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install whatsappy.

```bash
pip install whatsappy-py
```

## Usage

```python
from whatsappy import Whatsapp

whatsapp = Whatsapp()

whatsapp.login(visible=False) # Login whatsapp (Headless mode)

chat = whatsapp.chat('Mom') # Goes to the selected chat
chat.send('Hello') # Send a message

whatsapp.close() # Exit
```

You can find more examples [HERE](https://github.com/italoseara/whatsappy/tree/main/examples)

## Supported features

| Feature  | Status |
| ------------- | ------------- |
| Send messages  | ✅ |
| Receive messages  | ✅ |
| Send media (images/audio/documents)  | ✅ |
| Send media (video)  | ✅ |
| Send stickers | _pending_ |
| Receive media (images/audio/video/documents)  | ✅ |
| Send contact cards | _pending_ |
| Send location | _pending_ |
| Receive contact cards | ✅ | 
| Receive location | ✅ |
| Message replies | ✅ |
| Join groups by invite  | _pending_ |
| Get invite for group  | _pending_ |
| Modify group info (subject, description)  | ✅ |
| Modify group settings (send messages, edit info)  | _pending_ |
| Add group participants  | ✅ |
| Kick group participants  | ✅ |
| Promote group participants | ✅ |
| Demote group participants | ✅ |
| Mention users | ✅ |
| Mute/unmute chats | _pending_ |
| Block/unblock contacts | _pending_ |
| Get contact info | ✅ |
| Get group info | ✅ |
| Get profile pictures | ✅ |
| Set user status message | ✅ |

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://github.com/italoseara/whatsappy/blob/main/LICENSE)
