from __future__ import annotations

import requests
from PIL import Image
from PIL.JpegImagePlugin import JpegImageFile
from dataclasses import dataclass, field

from .. import chat
from .. import whatsapp
from ..util import *

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
    
    _whatsapp: whatsapp.Whatsapp = field(repr=False)
    
    name: str
    description: str
    participants: int
    profile_picture: JpegImageFile
    
    def __init__(self, _whatsapp: whatsapp.Whatsapp) -> None:
        super().__init__(_whatsapp)
        
        driver = self._whatsapp.driver
        
        # Group name
        self.name = emoji_to_text(driver.find_element(By.CSS_SELECTOR, Selectors.GROUP_SUBJECT))

        # Group description
        if read_more_btn := find_element_if_exists(driver, By.CSS_SELECTOR, Selectors.GROUP_READ_MORE):
            read_more_btn.click()

        if description_element := find_element_if_exists(driver, By.CSS_SELECTOR, Selectors.GROUP_DESCRIPTION):
            self.description = description_element.text
        else:
            self.description = None

        # Wait for the group participants to load
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, Selectors.GROUP_PARTICIPANTS)))
        
        # Group participants
        self.participants = int(driver.find_element(By.CSS_SELECTOR, Selectors.GROUP_PARTICIPANTS).text.split()[0])

        # Group profile picture
        if not element_exists(driver, By.CSS_SELECTOR, Selectors.GROUP_DEFAULT_PIC):
            pfp_url = driver.find_element(By.CSS_SELECTOR, Selectors.CHAT_INFO_PIC).get_attribute("src")
            self.profile_picture = Image.open(requests.get(pfp_url, stream=True).raw)
        else:
            self.profile_picture = None

    def leave(self, delete: bool = False) -> None:
        """Leaves the group.

        #### Arguments
            * delete (bool): Whether to delete the group or not.
        """

        if self._whatsapp.current_chat != self.name:
            raise NotSelectedException(f"The group \"{self.name}\" is not selected.")

        driver = self._whatsapp.driver
        driver.find_element(By.CSS_SELECTOR, Selectors.GROUP_LEAVE).click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, Selectors.POPUP_CONFIRM)))

        driver.find_element(By.CSS_SELECTOR, Selectors.POPUP_CONFIRM).click()

        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, Selectors.POPUP)))

        if delete:
            self.leave(delete=False)