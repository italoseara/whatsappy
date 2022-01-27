# whatsappy
[![Downloads](https://pepy.tech/badge/whatsappy-py)](https://pepy.tech/project/whatsappy-py)

Whatsappy is a Python library for creating whatsapp bots.

Creator: [Italo Seara](https://github.com/italoseara)

## Installation


Use the package manager [pip](https://pip.pypa.io/en/stable/) to install whatsappy.

```bash
pip install whatsappy-py
```

## Usage

### Basic example:
```python
from whatsappy import Whatsapp

whatsapp = Whatsapp()

whatsapp.login(visible=False) # Login whatsapp (Headless mode)

chat = whatsapp.chat('Mom') # Goes to the selected chat
chat.send('Hello') # Send a message

whatsapp.close() # Exit
```

## 1. Setup

```python
from whatsappy import Whatsapp

whatsapp = Whatsapp() # Initialize the library
```

## 2. Login

### Input
```python
whatsapp.login(visible=False, timeout=0)
```

| Arguments | Type | Default |
| --------- | ---- | ------- |
| visible   | bool | False   |
| timeout   | int  | 0       |

P.S: `timeout` should be in seconds

### Output
```
█████████████████████████████████████████████████████████████████
██ ▄▄▄▄▄ █▄███▀  ▄▄█ ▀▀█ ▄ ▄▄█▀ ██▄█▄▄▄█  ▀█▄    ▀█▄█  █ ▄▄▄▄▄ ██
██ █   █ █▄ ███▀ ▄█▄▀ █▄▄▀▀▀▄██▀▄█▄█▀ ▄█▀ ██▀▀██▀▀█  ▄ █ █   █ ██
██ █▄▄▄█ █▀▄ ▄▀██▀█▀    ▀▄▀█▀█ ▄▄▄ ███ ██  ██▀▀███▀▄ ▄██ █▄▄▄█ ██
██▄▄▄▄▄▄▄█▄▀ ▀ ▀▄█ █ █ ▀▄▀ ▀▄▀ █▄█ █▄▀ █▄▀▄█ ▀ █▄▀ ▀ █ █▄▄▄▄▄▄▄██
██ ▀▄█▀█▄▄█▄█▄  ██ ▀▀▄  █▄▀█ ▀▄▄▄  █▄█▄▄██ ▀▄▀ ▀▄▀▄ ▄ ▄▀█▄██ ▀ ██
██ █▀▄▄▀▄▄▄██▀▀▀▄ ██ ▄▄▄▀▀▀█ ▀▄█▄▄ ▀█▀█▀█▄ ▀▄▀█▄▀▀ ▄▄▄ ▄ █▄▄█▀ ██
██▄▄█ ▄▀▄▄ ▄██▄▀▀▀▀██▄██▄ █▀ ▄▄▀█▀ ▀█▀ █▄█▄▀▄▀▄▀▄▀  █▀█ ▄▀▄█▀█▀██
█████▄ █▄▄ ▀▀ ▄█▀█▄█▄▀█▀▄ ▀▀▀██ ▄ ▄█  ▄█▀ ██▀ █ ▄▄▄ ███  ▄█ ▄█ ██
██▀█▄█▄ ▄▀▄▄ ▄██  ▀▀▀█▀▀█▀▀▀▄▀█▄▀▀▄ █ ▄▀▄ ▄▀▄ ▄ ▄ ▄ █ ▄ ██▄█▄  ██
██▄▀█▀██▄  ▄▄██▀▀██▀ █▀ █   ▄▀▄ ▄▀▄ █ ▄ ▀▄ ▀█▄ ▄▄▀█ ▀█ █ ▄▀ █ ▄██
████ ▀▀▀▄▄▀▀▄▄▄▄   █ ▄▀▄▀██ ▄█▄▀ ▀ ▀█▀▄▄██ ▀▄ ▄▄▄▀▄▀▄ █ █▀  ▄ ███
██▄█▄ █▄▄▀▀ █ ▀██▄█ ▄▄▄▄▄█▄█ █▄ ▀▄ █▄ ▀▄█▄▀███▀██▄ █▄▄▀▄█▀ ▀▄█ ██
██ █▀▄▀ ▄█ ▄▄▀█▀ █▄   ▀▄▀█▄▀ █▄▄ ▄▄█▄▄▄█▄ ▄█▄▀▄█▄█▄▀▄▀██▄▄ ██  ██
██ ▄▄▄▀▀▄▀▄▄▀ ███ █▄▄▀ ▄ █▄ ▀▀▄ ██▀▀▄█ ▀▄▀▀▀▄▄▀█ ▀▄ ██▀▀█   ▄▀▄██
██  ▀▄ ▄▄▄ ██▀▄▀ █▄▄█▀█▄█ ▄▄   ▄▄▄ ▀█ ▄▄▄  ██▄▄ ▄█▄▀▄▀ ▄▄▄  █▄▄██
███▀ █ █▄█  █▄▀ █▀▀▀█▀▀▄▀█▄▄▄▄ █▄█  █████  ▀█▀▀▄ ▄  ▀█ █▄█  █▀▄██
██ ▀ ▀▄ ▄▄▄█▀ █▀   ▀▄▀▄ ▄ ▄▀▄▀▄▄▄  ▄▄█  ▄   ██▄▀▄█ ▀▄█   ▄▄███ ██
███ ▀█▀█▄▄█▀  ▀█ █▄█▄ ▀ ▀▄█▄  ██  ▄█▀▄█▀▄█▄▄ ▄█ ▄   ▄ ██ ██▀██ ██
███ ▄█ █▄█▀▀▄▄ ▀ ▄ ▀▀▄▀█▄▀█▀▄▀█▀ ▄▀▄██▀ ██▀ ▄█▀█▄ ▄▀█ █  ▀▄▄█▀▄██
██▀█▄▄ █▄██  █ ▄ ▀▄ █ ▀█▄█▀█▀ ▄ ▄███▀█▀█ ▀▀▄ ▀▀█▀▄█ ▄ ██  ▄▄▄████
██▀▀▄▄  ▄▀▀▄█▀▄ ▀▄ ▀█▀▄█▄  ██▀█▀▄▄▀ █▀ ▀██ ▀▄   ▄█▄▄▄ ▄▀ ▀▄▀█  ██
██▄  ▀█▀▄▀▄▄█ █▄▀█▀█▀█▀▀█ ▀▄▀ ██▄▀▄  ▀█ ▀ ▀▀  ▄▀ █▄█▀  ▀▄▀█▀▄  ██
██▄▀▄▀ █▄▄▄▀█▀▄██▀▀█▀▀▀▄▀ ▄▀ ▄ █ ▄▄ ▀▀  ▀ ▄ ▀█  ▀▀▄▄█ █▄█▀▄ █▀███
██ █ █ ▀▄████▀▀ ██▀▀▀▀▀█▀▄▄▀▀▀  ▄██   ▀▄▄▄▄ ▄▄▄  ▀▀▀▀  ▀▄▄█▄██ ██
██▀▄█ ▀▀▄▀ █▀█ ▀▀▀  █ ▄▀█ ▄█ ▀█ ▄▀▄ ▄ ▄▄▄█ ▀██▄▀█▄▄█▄▄▄ ▄▀█▄█▀▄██
██▀▀ ▄ ▄▄▄▀▀▀ █▄▀ ▀█ █▀ █▀▀ ▄   ██▄▀▄▀███     ▀▄ ████▀█▀▄▀▀▀▄█ ██
██▄▄▄▄██▄█▀▄ ██▀▀ ▄▀█ ▄▀█ ██▄█ ▄▄▄  █▀ █▄█ ▀▄▀ ▀█▀▄▀▄▄ ▄▄▄ ▄▄▀ ██
██ ▄▄▄▄▄ █▄█ ▀▀▀ ██▀█▄▀▀▄▀█▀▄  █▄█ ▀█▀▄▀█ ▄▀▄ ██ ▀▄▄▀▄ █▄█ ▀▄▀ ██
██ █   █ ██   ▄▀ ▄ ▀▀▀ ▄  █▀ ▄  ▄ ▄▀█ ▄ █ ▄▀█ ▄ ▄█  ▄▀   ▄ ▄▄████
██ █▄▄▄█ █▄▀██ ▄▀▀█▀██ ▄ ██ ▄▀▄▀▄▄▄ ▀▄  █▄ █▄  █▄▀ ▄█▀▄▀▄▀▄▄▄▄▄██
██▄▄▄▄▄▄▄█▄█▄█▄█▄██▄▄▄████▄▄▄█▄▄▄█▄███▄▄██▄▄██▄███▄█▄████▄████▄██
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
Scan the QRCode with your phone
```

### When you scan it, you should wait for a message like this:
```
Successfully logged in
```

## 3. Close

```python
whatsapp.close() # Closes the webdriver
```

## 4.1 Chat

### Input
```python
whatsapp.chat(name="Mom") # Opens the conversation
```

| Arguments | Type | Default |
| --------- | ---- | ------- |
| name      | str  | -       |

### Output


### *Group*

* Properties

  | Property        | Type | Default |
  | --------------- | ---- | ------- |
  | name            | str  | None    |
  | description     | str  | None    |
  | profile_picture | str  | None    |
  | invite_link     | str  | None    |
  | admin           | bool | False   |
  | last_message    | Any  | -       |

  P.S.: `last_message` will be explained later on

* Functions

  * `send` -> `None`: Sends a message to the chat
    
    | Arguments | Type | Default |
    | --------- | ---- | ------- |
    | message   | str  | ""      |
    | file      | str  | ""      |

    P.S.: `file` shoud be a file path
  
  * `add` -> `None`: Adds new participants to the group
  
    | Arguments | Type      | Default |
    | --------- | --------- | ------- |
    | contacts  | List[str] | -       | 

  * `remove` -> `None`: Removes participants from the group
  
    | Arguments | Type      | Default |
    | --------- | --------- | ------- |
    | contacts  | List[str] | -       |

  * `promote` -> `None`: Promotes participants to admin

    | Arguments | Type      | Default |
    | --------- | --------- | ------- |
    | contacts  | List[str] | -       |
  
  * `demote` -> `None`: Demotes participants to member

    | Arguments | Type      | Default |
    | --------- | --------- | ------- |
    | contacts  | List[str] | -       |
  
  * `leave` -> `None`: Leaves the group

    | Arguments | Type | Default |
    | --------- | ---- | ------- |
    | -         | -    | -       |

### *Contact*

* Properties
  
  | Property        | Type | Default |
  | --------------- | ---- | ------- |
  | name            | str  | None    |
  | number          | str  | None    |
  | about           | str  | None    |
  | profile_picture | str  | None    |
  | last_message    | Any  | -       |

  P.S.: `last_message` will be explained later on

* Functions

  * `send` -> `None`: Sends a message to the chat
    
    | Arguments | Type | Default |
    | --------- | ---- | ------- |
    | message   | str  | ""      |
    | file      | str  | ""      |

    P.S.: `file` shoud be a file path

## 4.2 Message

The `last_message` property of a chat will return the type of the message (Location, Text, Contact card, etc.) as a class, it can be:

### *Text*

* Properties

  | Property     | Type     | Default |
  | ------------ | -------- | ------- |
  | text         | str      | ""      |
  | chat         | Any      | None    |
  | author       | str      | None    |
  | time         | datetime | None    |
  | forwarded    | bool     | False   |
  | quote        | Quote    | -       |
  | Quote.text   | str      | -       |
  | Quote.author | str      | -       |

* Functions

  * `forward` -> `None`: Forward the message to a list of contacts

    | Arguments | Type      | Default |
    | --------- | --------- | ------- |
    | contacts  | List[str] | -       |
  
  * `reply` -> `None`: Reply the message quoting the original one

    | Arguments | Type | Default |
    | --------- | ---- | ------- |
    | message   | str  | ""      |
    | file      | str  | ""      |

    P.S.: `file` should be a file path

  * `reply_privately` -> `None`: Reply the message in private chat (Only works on groups)

    | Arguments | Type | Default |
    | --------- | ---- | ------- |
    | message   | str  | ""      |
    | file      | str  | ""      |

    P.S.: `file` should be a file path

  * `delete` -> `None`: Deletes the message only for you

    | Arguments | Type | Default |
    | --------- | ---- | ------- |
    | -         | -    | -       |

  * `star` -> `None`: Stars the message for you

    | Arguments | Type | Default |
    | --------- | ---- | ------- |
    | -         | -    | -       |

### *Document*

Inherits all the `Text` properties and functions

* Properties

  | Arguments     | Type  | Default |
  | ------------- | ----- | ------- |
  | file          | File  | None    |
  | File.size     | int   | 0       |
  | File.name     | str   | ""      |
  | File.mimetype | str   | ""      |
  | File.content  | bytes | b""     |

### *Video*

Inherits all the `Text` properties and functions

* Properties

  | Arguments | Type | Default |
  | --------- | ---- | ------- |
  | length    | int  | 0       |

### *Audio*

Inherits all the `Text` properties and functions

* Properties

  | Arguments    | Type  | Default |
  | ------------ | ----- | ------- |
  | file         | File  | None    |
  | File.size    | int   | 0       |
  | File.length  | int   | 0       |
  | File.content | bytes | b""     |
  | isrecorded   | bool  | False   |

### *ContactCard*

Inherits all the `Text` properties and functions

* Properties

  | Arguments       | Type          | Default |
  | --------------- | ------------- | ------- |
  | contacts        | List[Contact] | []      |
  | Contact.name    | str           | ""      |
  | Contact.numbers | List[str]     | []      |

### *Location*

Inherits all the `Text` properties and functions

* Properties

  | Arguments | Type  | Default |
  | --------- | ----- | ------- |
  | coords    | tuple | ()      |
  | link      | str   | ""      |

### *LiveLocation*

Inherits all the `Location` properties and functions

* Properties

  | Arguments | Type     | Default |
  | --------- | -------- | ------- |
  | until     | datetime | None    |

### Image

Inherits all the `Text` properties and functions

* Properties

  | Arguments       | Type  | Default |
  | --------------- | ----- | ------- |
  | file            | File  | None    |
  | File.size       | int   | 0       |
  | File.resolution | tuple | ()      |
  | File.content    | bytes | b""     |

### Sticker

Inherits all the `Image` properties and functions

* Properties

  | Arguments | Type | Default |
  | --------- | ---- | ------- |
  | -         | -    | -       |



## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://github.com/italoseara/whatsappy/blob/main/LICENSE)
