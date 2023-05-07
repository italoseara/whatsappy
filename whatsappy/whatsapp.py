from __future__ import annotations

import os
from time import sleep
from qrcode import QRCode
from typing import Dict, List, Callable, Self

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from .util import *
from .chat import *
from .messages import *

class Whatsapp:
    """The main class for interacting with WhatsApp web.

    #### Arguments
        * timeout (int, optional): The time to wait for the page to load. Defaults to 60.
        * visible (bool, optional): Whether the browser should be visible or not. Defaults to True.
        * data_path (str, optional): The path to the Chrome data directory (it is used to save the session). Defaults to None.
        * chrome_options (Options, optional): The options for the Chrome driver. Defaults to None.

    #### Properties:
        * driver (webdriver.Chrome): The Chrome driver.
        * unread_messages (List[Unread]): List of unread messages.

    #### Methods:
        * run: Starts the WhatsApp web session.
        * close: Closes the WhatsApp web session.
        * open: Opens a chat with the specified name or phone number.
    """

    driver: webdriver.Chrome

    _timeout: int
    _visible: bool
    _data_path: str
    _chrome_options: Options

    _callbacks: Dict[str, Callable] = {
        "on_ready": None,
        "on_message": None
    }
    _threads: Dict[str, MyThread] = {
        "on_message": None
    }

    def __init__(self, timeout: int = 60, visible: bool = True, data_path: str = None, chrome_options: Options = None) -> None:
        self._timeout = timeout
        self._visible = visible
        self._data_path = data_path
        self._chrome_options = chrome_options

    def run(self) -> Self:
        """Starts the WhatsApp web session.

        #### Returns
            * Self: The current instance of the class.
        """

        # Chrome options
        self._chrome_options = self._chrome_options or Options()
        self._chrome_options.add_argument("--start-maximized")

        if not self._visible:
            self._chrome_options.add_argument("--headless")
            self._chrome_options.add_argument("--window-size=1920,1080")

        if self._data_path:
            self._chrome_options.add_argument(f"--user-data-dir={self._data_path}")

        # Disable the logging
        self._chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

        # Open the browser
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self._chrome_options)

        # Open the WhatsApp web page
        self.driver.get("https://web.whatsapp.com/")

        # Wait until the page is loaded
        WebDriverWait(self.driver, self._timeout).until(lambda driver: (
            element_exists(self.driver, By.CSS_SELECTOR, Selectors.QR_CODE) or
            element_exists(self.driver, By.CSS_SELECTOR, Selectors.SEARCH_BAR)
        ))

        qr_code = find_element_if_exists(self.driver, By.CSS_SELECTOR, Selectors.QR_CODE)

        if qr_code:
            if not self._visible:
                data_ref = qr_code.get_attribute("data-ref")

                os.system("cls||clear")

                qr = QRCode(version=1, border=2)
                qr.add_data(data_ref)
                qr.make(fit=True)
                qr.print_ascii(invert=True)

            print("Scan the QR code with your phone to log in.")

        WebDriverWait(self.driver, self._timeout).until(lambda driver: self._is_loaded())
        sleep(1) # Sometimes the page is not loaded correctly

        # Create the threads
        self._threads["on_ready"] = MyThread(target=self._on_ready, daemon=True)
        self._threads["on_message"] = MyThread(target=self._on_message, daemon=True)

        # Start the threads
        for thread in self._threads.values():
            thread.start()

        return self

    @property
    def current_chat(self) -> str | None:
        """Returns the name of the current chat.

        #### Returns
            * str: The name of the current chat.
            * None: If there is no chat open.
        """

        current_chat = find_element_if_exists(self.driver, By.CSS_SELECTOR, Selectors.CURRENT_CHAT)

        if not current_chat:
            return None

        return emoji_to_text(current_chat)

    @property
    def unread_messages(self) -> List[UnreadMessage]:
        """Returns the list of unread messages in the conversations page.

        #### Returns
            * List[UnreadMessage]: List of unread messages.
        """

        return [UnreadMessage(self, element) for element in self.driver.find_elements(By.XPATH, Selectors.UNREAD_CONVERSATIONS_XPATH)]

    @property
    def me(self) -> Me:
        """Returns the current user.

        #### Returns
            * Me: The current user.
        """

        return Me(self)

    def open(self, chat: str) -> (Chat | Group | None):
        """Opens a chat with the specified name or phone number

        #### Arguments
            * chat (str): The name or phone number of the chat to open

        #### Returns
            * (Chat | Group | None): The chat with the specified name or phone number. None if the chat wasn't found
        """

        if not self._is_loaded():
            raise Exception("Something went wrong while loading WhatsApp web.")

        if phone_number_regex.match(chat):
            # Remove all the non-numeric characters
            phone = "".join(filter(str.isdigit, chat))

            self.driver.get(f"https://web.whatsapp.com/send?phone={phone}")
            WebDriverWait(self.driver, 5).until(lambda driver: self._is_loaded())
        else:
            # Close the menu and the current chat
            ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
            WebDriverWait(self.driver, 5).until(lambda driver: not self._is_animating())
            ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()

            search = self.driver.find_element(By.CSS_SELECTOR, Selectors.SEARCH_BAR)
            send_keys_slowly(search, chat)
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, Selectors.SEARCH_BAR_CLEAR))
            )
            search.send_keys(Keys.ENTER)

            # Clear the search bar
            self.driver.find_element(By.CSS_SELECTOR, Selectors.SEARCH_BAR_CLEAR).click()

        # Open the chat info
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, Selectors.CONVERSATION_HEADER))
            )
            self.driver.find_element(By.CSS_SELECTOR, Selectors.CONVERSATION_HEADER).click()
        except TimeoutException:
            return None

        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, Selectors.INFO_DRAWER_BODY)))

        if element_exists(self.driver, By.CSS_SELECTOR, Selectors.GROUP_INFO_HEADER):
            return Group(self)

        return Chat(self)

    def event(self, func: Callable) -> None:
        """Decorator to register a function as an event handler.

        #### Arguments
            * func: The function to be registered. It must be a coroutine.

        Raises:
            * InvalidEvent: If the function name is not a valid event.
        """

        if func.__name__ not in self._callbacks.keys():
            raise InvalidEventException(f"Invalid event: {func.__name__}")

        self._callbacks[func.__name__] = func

    def close(self) -> None:
        """Closes the browser window and stops all running threads."""

        for key in self._callbacks.keys():
            self._callbacks[key] = None

        for thread in self._threads.values():
            thread.stop()

        self.driver.close()

    def _on_ready(self) -> None:
        """Calls the on_ready callback when the page is loaded."""

        if not self._callbacks["on_ready"]:
            return

        self._callbacks["on_ready"]()

    def _on_message(self) -> None:
        """Checks for new messages and calls the on_message callback"""

        last_check = self.unread_messages

        while True:
            if self._threads["on_message"].stopped():
                break

            if not self._callbacks["on_message"]:
                continue

            try:
                unread = self.unread_messages
            except StaleElementReferenceException:
                continue

            for chat in unread:
                if chat not in last_check and chat.message is not None:
                    self._callbacks["on_message"](chat)

            last_check = unread
            sleep(1) # Wait 1 second before checking again

    def _is_loaded(self) -> bool:
        """Check if the page is loaded."""

        try:
            return element_exists(self.driver, By.CSS_SELECTOR, Selectors.SEARCH_BAR)
        except Exception:
            return False

    def _is_animating(self) -> bool:
        """Check if the page is animating."""

        return element_exists(self.driver, By.CSS_SELECTOR, Selectors.ANIMATING)
