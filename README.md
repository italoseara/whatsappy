# whatsappy

Whatsappy is a Python library for creating whatsapp bots.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install whatsappy.

```bash
pip install whatsappy (not working yet)
```

Than install the requeriments using:
```bash
pip install -r requeriments.txt
```

## Usage

```python
from whatsappy.wpp import whatsapp

whatsapp.login() # Login on whatsapp

whatsapp.select_chat('Mom') # Goes to the selected chat
whatsapp.send('Hello') # send a message
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/) (not done yet)