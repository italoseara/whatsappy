from __future__ import annotations

import os
from qrcode import QRCode
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from . import util
from .util import Selectors

from .chat import Chat

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
            util.element_exists(self.driver, By.CSS_SELECTOR, Selectors.CHAT_LIST_SEARCH)
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
        print("Logged in successfully.")
        sleep(2) # Safety sleep

    def is_loaded(self) -> bool:
        """Check if the page is loaded."""
        
        return util.element_exists(self.driver, By.CSS_SELECTOR, Selectors.CHAT_LIST_SEARCH)
    
    def get_chat(self, chat_name: str) -> Chat:
        """Get a chat by its name.

        Args:
            chat_name (str): The name of the chat.

        Returns:
            Chat: The chat.
        """
        
        return Chat(self, chat_name)

    def close(self) -> None:
        """Close the web driver."""
        
        self.driver.close()
