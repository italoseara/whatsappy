from __future__ import annotations

from time import sleep

from .. import whatsapp, util
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

    def __init__(self, _whatsapp: whatsapp.Whatsapp, name: str) -> None:
        """Initializes the chat."""
        
        self._whatsapp = _whatsapp
        self.name = name

        self.open()

    def open(self) -> None:
        """Opens the chat."""

        driver = self._whatsapp.driver

        if not self._whatsapp.is_loaded():
            raise Exception("Something went wrong while loading WhatsApp web.")

        search = driver.find_element(By.CSS_SELECTOR, Selectors.SEARCH_BAR)
        
        search.clear()
        search.send_keys(self.name)
        search.send_keys(Keys.ENTER)

        WebDriverWait(driver, 5).until(lambda driver: util.element_exists(driver, By.CSS_SELECTOR, Selectors.SEARCH_BAR_CLEAR))

        driver.find_element(By.CSS_SELECTOR, Selectors.SEARCH_BAR_CLEAR).click()
