from __future__ import annotations

from dataclasses import dataclass

import requests
from PIL import Image
from PIL.JpegImagePlugin import JpegImageFile
from dataclasses import dataclass, field
from typing import List

from . import Conversation
from .. import whatsapp
from ..util import *

from selenium.webdriver.common.by import By

@dataclass(init=False)
class Group(Conversation):
    """A group in WhatsApp.

    Properties:
        subject (str): The subject of the group.
        description (str): The description of the group.
        profile_picture (JpegImageFile): The profile picture of the group.
        participants (List[str]): The participants of the group.
        starred_messages (List[str]): The starred messages of the group.
    """

    subject: str
    description: str
    profile_picture: JpegImageFile
    participants: List[str]
    
    def __init__(self, _whatsapp: whatsapp.Whatsapp) -> None:
        super().__init__(_whatsapp)
        
        driver = self._whatsapp.driver

        self.subject = driver.find_element(By.CSS_SELECTOR, Selectors.GROUP_SUBJECT).get_attribute("title")

        if element_exists(driver, By.CSS_SELECTOR, Selectors.GROUP_DEFAULT_PIC):
            self.profile_picture = None
        else:
            pfp_url = driver.find_element(By.CSS_SELECTOR, Selectors.CHAT_INFO_PIC).get_attribute("src")
            self.profile_picture = Image.open(requests.get(pfp_url, stream=True).raw)

        # TODO:
        self.description = None
        self.participants = None
        self.profile_picture = None