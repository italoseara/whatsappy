from __future__ import annotations

import requests
from PIL import Image
from PIL.JpegImagePlugin import JpegImageFile
from dataclasses import dataclass

from selenium.webdriver.common.by import By

from . import Conversation
from .. import whatsapp
from ..util import *

@dataclass(init=False)
class Chat(Conversation):
    """A chat in WhatsApp. Should not be initialized directly, use `whatsappy.Whatsapp.open` instead.

    Properties:
        name (str): The name of the chat.
        
        number (str): The number of the chat.

        about (str): The about of the chat.

        profile_picture (JpegImageFile): The profile picture of the chat.

        starred_messages (List[str]): The starred messages of the chat.
    """

    name: str
    number: str
    about: str
    profile_picture: JpegImageFile

    def __init__(self, _whatsapp: whatsapp.Whatsapp) -> None:
        super().__init__(_whatsapp)

        driver = self._whatsapp.driver

        info = driver.find_elements(By.CSS_SELECTOR, Selectors.CHAT_INFO_TEXT)

        self.name = info[0].text
        self.number = info[1].text
        self.about = info[2].get_attribute("title") if len(info) > 2 else None

        if self.number.startswith("~"):
            self.name, self.number = self.number[1:], self.name

        if element_exists(driver, By.CSS_SELECTOR, Selectors.CHAT_DEFAULT_PIC):
            self.profile_picture = None
        else:
            pfp_url = driver.find_element(By.CSS_SELECTOR, Selectors.CHAT_INFO_PIC).get_attribute("src")
            self.profile_picture = Image.open(requests.get(pfp_url, stream=True).raw)