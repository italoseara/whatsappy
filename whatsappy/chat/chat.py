from __future__ import annotations

from time import sleep

from .. import whatsapp
from ..util import Selectors

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait

class Chat:
    """A chat in WhatsApp.

    Args:
        whatsapp (Whatsapp): The whatsapp instance.
        chat_name (str): The name of the chat.
    """

    _whatsapp: whatsapp.Whatsapp
    name: str
    number: str
    about: str
    profile_picture: str

    def __init__(self, _whatsapp: whatsapp.Whatsapp, chat_name: str) -> None:
        """Initializes the chat."""
        
        self._whatsapp = _whatsapp

        # Open the chat
        self.open(chat_name)

        # Get the info needed
        

    def open(self, chat_name: str) -> None:
        """Opens the chat."""

        driver = self._whatsapp.driver

        if not self._whatsapp.is_loaded():
            raise Exception("Something went wrong while loading WhatsApp web.")

        driver.find_element(By.CSS_SELECTOR, Selectors.NEW_CHAT).click()

        search_bar = driver.find_element(By.CSS_SELECTOR, Selectors.CHAT_LIST_SEARCH)

        # Search for the chat and open it
        search_bar.clear()
        search_bar.send_keys(chat_name)
        sleep(0.1)
        search_bar.send_keys(Keys.ENTER)
