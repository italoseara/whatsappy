from __future__ import annotations

import os
from qrcode import QRCode
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from . import util
from .util import Selectors

from .chat import *

class Whatsapp:
    """The main class for interacting with WhatsApp web.

    Args:
        timeout (int, optional): The time to wait for the page to load. Defaults to 60.
        visible (bool, optional): Whether the browser should be visible or not. Defaults to True.
        data_path (str, optional): The path to the Chrome data directory (it is used to save the session). Defaults to None.
        chrome_options (Options, optional): The options for the Chrome driver. Defaults to None.
    """
    
    driver: webdriver.Chrome
    actions: ActionChains

    def __init__(self, timeout: int = 60, visible: bool = True, data_path: str = None, chrome_options: Options = None) -> None:
        """Initializes the browser and logs in to WhatsApp web."""

        # Chrome options
        options = chrome_options or Options()
        options.add_argument("--headless" if not visible else "--start-maximized")

        if data_path:
            options.add_argument(f"--user-data-dir={data_path}")

        # Disable the logging
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        
        # Open the browser
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        # Open the WhatsApp web page
        self.driver.get("https://web.whatsapp.com/")

        # Wait until the page is loaded
        WebDriverWait(self.driver, timeout).until(lambda driver: (
            util.element_exists(self.driver, By.CSS_SELECTOR, Selectors.QR_CODE) or
            util.element_exists(self.driver, By.CSS_SELECTOR, Selectors.SEARCH_BAR)
        ))

        qr_code = util.find_element_if_exists(self.driver, By.CSS_SELECTOR, Selectors.QR_CODE)

        if qr_code:
            if not visible:
                data_ref = qr_code.get_attribute("data-ref")

                os.system("cls||clear")
                
                qr = QRCode(version=1, border=2)
                qr.add_data(data_ref)
                qr.make(fit=True)
                qr.print_ascii(invert=True)

            print("Scan the QR code with your phone to log in.")

        WebDriverWait(self.driver, timeout).until(lambda driver: self.is_loaded())
        sleep(1) # Sometimes the page is not loaded correctly

    def is_loaded(self) -> bool:
        """Check if the page is loaded."""
        
        return util.element_exists(self.driver, By.CSS_SELECTOR, Selectors.SEARCH_BAR)

    def is_animating(self) -> bool:
        """Check if the page is animating."""

        return util.element_exists(self.driver, By.CSS_SELECTOR, Selectors.ANIMATING)

    def open(self, name: str) -> Chat | GroupChat | None:
        """Get a chat by its name.

        Args:
            name (str): The name of the chat.

        Returns:
            Chat | GroupChat | None: The chat or None if it does not exist.
        """

        if not self.is_loaded():
            raise Exception("Something went wrong while loading WhatsApp web.")

        if util.phone_number_regex.match(name):
            # Remove all the non-numeric characters
            phone = "".join(filter(str.isdigit, name))
            
            self.driver.get(f"https://web.whatsapp.com/send?phone={phone}")
            WebDriverWait(self.driver, 5).until(lambda driver: self.is_loaded())
        else:
            # Close the menu and the current chat
            ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
            WebDriverWait(self.driver, 5).until(lambda driver: not self.is_animating())
            ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()

            search = self.driver.find_element(By.CSS_SELECTOR, Selectors.SEARCH_BAR)            
            search.send_keys(name)
            WebDriverWait(self.driver, 5).until(lambda driver: util.element_exists(driver, By.CSS_SELECTOR, Selectors.SEARCH_BAR_CLEAR))
            sleep(0.5) # Sometimes the search bar is not loaded correctly
            search.send_keys(Keys.ENTER)

            # Clear the search bar
            self.driver.find_element(By.CSS_SELECTOR, Selectors.SEARCH_BAR_CLEAR).click()

        # Open the chat info
        try:
            WebDriverWait(self.driver, 5).until(lambda driver: util.element_exists(driver, By.CSS_SELECTOR, Selectors.CHAT_HEADER))
            self.driver.find_element(By.CSS_SELECTOR, Selectors.CHAT_HEADER).click()
        except TimeoutException:
            return None
        
        WebDriverWait(self.driver, 5).until(lambda driver: 
            not self.is_animating() and 
            len(self.driver.find_elements(By.CSS_SELECTOR, Selectors.CHAT_INFO_TEXT)) > 0
        )

        if util.element_exists(self.driver, By.CSS_SELECTOR, Selectors.GROUP_SUBJECT):
            return GroupChat(self)
        
        return Chat(self)

    def close(self) -> None:
        """Close the web driver."""
        
        self.driver.close()
