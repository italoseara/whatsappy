from __future__ import annotations

import requests
from PIL import Image
from PIL.JpegImagePlugin import JpegImageFile
from dataclasses import dataclass, field

from .. import whatsapp, util
from ..util import Selectors

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait

@dataclass(init=False)
class Chat:
    """A chat in WhatsApp.

    Attributes:
        name (str): The name of the chat.
        number (str): The number of the chat.
        about (str): The about of the chat.
        profile_picture (JpegImageFile): The profile picture of the chat.
    """

    _whatsapp: whatsapp.Whatsapp = field(repr=False)
    name: str
    number: str
    about: str
    profile_picture: JpegImageFile

    def __init__(self, _whatsapp: whatsapp.Whatsapp) -> None:
        """Initializes the chat."""

        driver = _whatsapp.driver
        self._whatsapp = _whatsapp

        info = driver.find_elements(By.CSS_SELECTOR, Selectors.CHAT_INFO_TEXT)

        self.name = info[0].text
        self.number = info[1].text

        if len(info) > 2:
            self.about = info[2].text
        else:
            self.about = None

        if self.number.startswith("~"):
            self.name, self.number = self.number[1:], self.name

        if util.element_exists(driver, By.CSS_SELECTOR, Selectors.CHAT_DEFAULT_USER):
            self.profile_picture = None

        pfp_url = driver.find_element(By.CSS_SELECTOR, Selectors.CHAT_INFO_PICTURE).get_attribute("src")
        self.profile_picture = Image.open(requests.get(pfp_url, stream=True).raw)

