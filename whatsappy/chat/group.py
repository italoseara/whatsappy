from __future__ import annotations

from dataclasses import dataclass

import requests
from PIL import Image
from PIL.JpegImagePlugin import JpegImageFile
from dataclasses import dataclass
from typing import List

from .. import chat
from .. import whatsapp
from ..util import *

from selenium.webdriver.common.by import By

@dataclass(init=False)
class Group(chat.Conversation):
    """A group in WhatsApp. Should not be initialized directly, use `whatsappy.Whatsapp.open` instead.

    #### Properties
        * subject (str): The subject of the group.
        * description (str): The description of the group.
        * profile_picture (JpegImageFile): The profile picture of the group.
        * participants (int): The number of participants of the group.
        * starred_messages (List[str]): The starred messages of the group.
    """

    name: str
    description: str
    participants: int
    profile_picture: JpegImageFile
    
    def __init__(self, _whatsapp: whatsapp.Whatsapp) -> None:
        super().__init__(_whatsapp)
        
        driver = self._whatsapp.driver
        
        # Group name
        self.name = driver.find_element(By.CSS_SELECTOR, Selectors.GROUP_SUBJECT).get_attribute("title")

        # Group description
        if read_more_btn := find_element_if_exists(driver, By.CSS_SELECTOR, Selectors.GROUP_READ_MORE):
            read_more_btn.click()

        if description_element := find_element_if_exists(driver, By.CSS_SELECTOR, Selectors.GROUP_DESCRIPTION):
            self.description = description_element.text
        else:
            self.description = None

        # Group participants
        self.participants = int(driver.find_element(By.CSS_SELECTOR, Selectors.GROUP_PARTICIPANTS).text.split()[0])

        # Group profile picture
        if not element_exists(driver, By.CSS_SELECTOR, Selectors.GROUP_DEFAULT_PIC):
            pfp_url = driver.find_element(By.CSS_SELECTOR, Selectors.CHAT_INFO_PIC).get_attribute("src")
            self.profile_picture = Image.open(requests.get(pfp_url, stream=True).raw)
        else:
            self.profile_picture = None
