from __future__ import annotations

import os
from time import sleep
from qrcode import QRCode
from threading import Thread
from typing import Dict, List, Callable

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from .util import *
from .chat import *

class Whatsapp:
    """The main class for interacting with WhatsApp web.

    Args:
        timeout (int, optional): The time to wait for the page to load. Defaults to 60.
        visible (bool, optional): Whether the browser should be visible or not. Defaults to True.
        data_path (str, optional): The path to the Chrome data directory (it is used to save the session). Defaults to None.
        chrome_options (Options, optional): The options for the Chrome driver. Defaults to None.
    """

    _on_message_callback: Callable[[str], None] = None
    _threads: Dict[str, MyThread] = {}
    
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
            element_exists(self.driver, By.CSS_SELECTOR, Selectors.QR_CODE) or
            element_exists(self.driver, By.CSS_SELECTOR, Selectors.SEARCH_BAR)
        ))

        qr_code = find_element_if_exists(self.driver, By.CSS_SELECTOR, Selectors.QR_CODE)

        if qr_code:
            if not visible:
                data_ref = qr_code.get_attribute("data-ref")

                os.system("cls||clear")
                
                qr = QRCode(version=1, border=2)
                qr.add_data(data_ref)
                qr.make(fit=True)
                qr.print_ascii(invert=True)

            print("Scan the QR code with your phone to log in.")

        WebDriverWait(self.driver, timeout).until(lambda driver: self._is_loaded())
        sleep(1) # Sometimes the page is not loaded correctly

        print(self.unread_messages)

        # Create the threads
        self._threads["on_message"] = MyThread(target=self._look_for_messages, daemon=True)

        # Start the threads
        for thread in self._threads.values():
            thread.start()

    @property
    def unread_messages(self) -> List[UnreadChat]:
        """Get the unread messages.

        Returns:
            Dict[str, int]: The unread messages.
        """

        unread = []
        elements = self.driver.find_elements(By.XPATH, Selectors.XPATH_UNREAD_CONVERSATIONS)

        for element in elements:
            title = element.find_element(By.CSS_SELECTOR, Selectors.UNREAD_TITLE).get_attribute("title")
            number = element.find_element(By.CSS_SELECTOR, Selectors.UNREAD_BADGE).text or 1
            last_message = element.find_element(By.CSS_SELECTOR, Selectors.UNREAD_LAST_MESSAGE).get_attribute("title")

            unread.append(UnreadChat(title, number, last_message))

        return unread

    def _look_for_messages(self) -> None:
        """Look for new messages."""

        last_check = self.unread_messages

        while True:
            if self._threads["on_message"].stopped():
                break
            
            if self._on_message_callback:
                unread = self.unread_messages

                for chat in unread:
                    if chat not in last_check:
                        self._on_message_callback(chat)

                unread = last_check
            sleep(1)

    def _is_loaded(self) -> bool:
        """Check if the page is loaded."""

        try:
            return element_exists(self.driver, By.CSS_SELECTOR, Selectors.SEARCH_BAR)
        except Exception:
            return False

    def _is_animating(self) -> bool:
        """Check if the page is animating."""

        return element_exists(self.driver, By.CSS_SELECTOR, Selectors.ANIMATING)

    def open(self, name: str) -> Chat | Group | None:
        """Get a chat by its name.

        Args:
            name (str): The name of the chat.

        Returns:
            Chat | GroupChat | None: The chat or None if it does not exist.
        """

        if not self._is_loaded():
            raise Exception("Something went wrong while loading WhatsApp web.")

        if phone_number_regex.match(name):
            # Remove all the non-numeric characters
            phone = "".join(filter(str.isdigit, name))
            
            self.driver.get(f"https://web.whatsapp.com/send?phone={phone}")
            WebDriverWait(self.driver, 5).until(lambda driver: self._is_loaded())
        else:
            # Close the menu and the current chat
            ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
            WebDriverWait(self.driver, 5).until(lambda driver: not self._is_animating())
            ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()

            search = self.driver.find_element(By.CSS_SELECTOR, Selectors.SEARCH_BAR)            
            send_keys_slowly(search, name, delay=0.01)
            WebDriverWait(self.driver, 5).until(lambda driver: element_exists(driver, By.CSS_SELECTOR, Selectors.SEARCH_BAR_CLEAR))
            search.send_keys(Keys.ENTER)

            # Clear the search bar
            self.driver.find_element(By.CSS_SELECTOR, Selectors.SEARCH_BAR_CLEAR).click()

        # Open the chat info
        try:
            WebDriverWait(self.driver, 5).until(lambda driver: element_exists(driver, By.CSS_SELECTOR, Selectors.CHAT_HEADER))
            self.driver.find_element(By.CSS_SELECTOR, Selectors.CHAT_HEADER).click()
        except TimeoutException:
            return None
        
        WebDriverWait(self.driver, 5).until(lambda driver: 
            not self._is_animating() and 
            len(self.driver.find_elements(By.CSS_SELECTOR, Selectors.CHAT_INFO_TEXT)) > 0
        )

        if element_exists(self.driver, By.CSS_SELECTOR, Selectors.GROUP_SUBJECT):
            return Group(self)
        
        return Chat(self)
    
    def on_message(self, func: Callable[[UnreadChat], None]) -> callable:
        """Decorator to set the on message callback.

        Args:
            func (Callable[[str], None]): The function to call when a new message is received.

        Usage:
            @whatsapp.on_message
            def foo(chat_name: str):
                print(chat_name)
        """

        self._on_message_callback = func 

    def close(self) -> None:
        """Close the web driver."""
        
        self.driver.close()

        for thread in self._threads.values():
            thread.stop()
