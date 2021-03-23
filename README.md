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

whatsapp.login() # Login whatsapp

whatsapp.select_chat('Mom') # Goes to the selected chat
whatsapp.send('Hello') # Send a message

whatsapp.exit() # Exit
```

You can find more examples [HERE](https://github.com/italoseara/whatsappy/tree/main/examples)

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://github.com/italoseara/whatsappy/blob/main/LICENSE)
