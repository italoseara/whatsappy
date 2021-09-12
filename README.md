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
from whatsappy import whatsapp

whatsapp.login(visible=False) # Login whatsapp (Headless mode)

whatsapp.select_chat('Mom') # Goes to the selected chat
whatsapp.send('Hello') # Send a message

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
| Receive location | ✅ | 
| Message replies | ✅ |
| Join groups by invite  | _pending_ |
| Get invite for group  | ✅ |
| Modify group info (subject, description)  | ✅ |
| Modify group settings (send messages, edit info)  | ✅ |
| Add group participants  | ✅ |
| Kick group participants  | ✅ |
| Promote group participants | ✅ |
| Demote group participants | _pending_ |
| Mention users | ✅ |
| Mute/unmute chats | _pending_ |
| Block/unblock contacts | _pending_ |
| Get contact info | _pending_ |
| Get profile pictures | _pending_ |
| Set user status message | _pending_ |

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://github.com/italoseara/whatsappy/blob/main/LICENSE)
