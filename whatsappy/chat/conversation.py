from __future__ import annotations

import os
from time import sleep
from dataclasses import dataclass, field
from typing import List, Literal, Tuple

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from .. import whatsapp
from ..messages import Message
from ..util import *

@dataclass(init=False)
class Conversation:
    """Utility class for conversations and groups. Should not be initialized directly, use `whatsappy.Whatsapp.open` instead."""
    
    _whatsapp: whatsapp.Whatsapp = field(repr=False)
    name: str

    def __init__(self, _whatsapp: whatsapp.Whatsapp) -> None:
        self._whatsapp = _whatsapp

    @property
    def last_message(self) -> Message | None:
        """Returns the last message in the conversation."""

        if self._whatsapp.current_chat != self.name:
            raise NotSelectedException(f"The chat \"{self.name}\" is not selected.")

        messages = self._whatsapp.driver.find_elements(By.CSS_SELECTOR, Selectors.CONVERSATION_MESSAGES)

        if not messages:
            return None

        last_element = messages[-1]
        
        return Message(self._whatsapp, last_element, self)

    @property
    def is_muted(self) -> bool:
        """Returns whether the conversation is muted or not."""

        if self._whatsapp.current_chat != self.name:
            raise NotSelectedException(f"The chat \"{self.name}\" is not selected.")

        return element_exists(self._whatsapp.driver, By.CSS_SELECTOR, Selectors.CONVERSATION_MUTED)

    @property
    def is_pinned(self) -> bool:
        """Returns whether the conversation is pinned or not."""

        if self._whatsapp.current_chat != self.name:
            raise NotSelectedException(f"The chat \"{self.name}\" is not selected.")

        _, is_pinned = self._is_pinned()
        self._whatsapp._clear_search_bar()

        return is_pinned
    
    def send(self, 
             message: str = None, 
             attatchments: List[str] = None, 
             type: Literal["auto", "document", "midia", "contact"] = "auto"
        ) -> None:
        """Sends a message to the conversation.

        #### Arguments
            * message (str, optional): The message to send. Defaults to None.
            * attatchments (List[Any], optional): The attatchments to send. Defaults to None.
            * type (Literal["auto", "document", "midia", "contact"], optional): The type of the attatchments. Defaults to "auto".
            If the type is specified, all the attatchments must be of the same type.

        #### Raises
            * NotSelectedException: If the conversation is not selected.
            * ValueError: If no attatchments or message are specified.
            * TypeError: If any of the attatchments is not a string.
            * FileNotFoundError: If any of the attatchments is a file that does not exist.
            * ContactNotFoundException: If any of the contacts does not exist.
        """

        if self._whatsapp.current_chat != self.name:
            raise NotSelectedException(f"The chat \"{self.name}\" is not selected.")

        driver = self._whatsapp.driver

        if not attatchments and not message:
            raise ValueError("You must specify at least one attatchment or a message.")

        if type not in ["auto", "document", "midia", "contact"]:
            raise ValueError("The type must be one of the following: auto, document, midia, contact.")

        if not attatchments:
            msg_box = driver.find_element(By.CSS_SELECTOR, Selectors.MESSAGE_BOX)
            send_keys_multiline(msg_box, message)
            msg_box.send_keys(Keys.ENTER)
            return
        
        # Check if the attatchments are valid:
        for attatchment in attatchments:
            if not isinstance(attatchment, str):
                raise TypeError(f"The attatchment {attatchment} is not a string.")
            elif "." in attatchment and not os.path.isfile(attatchment):
                raise FileNotFoundError(f"The file {attatchment} does not exist.")

        attatchment_types = {attatchment: type if type != "auto" else get_attachment_type(attatchment) for attatchment in attatchments}

        documents = [attatchment for attatchment, type in attatchment_types.items() if type == "document"]
        midias = [attatchment for attatchment, type in attatchment_types.items() if type == "midia"]
        contacts = [attatchment for attatchment, type in attatchment_types.items() if type == "contact"]

        if contacts:
            driver.find_element(By.CSS_SELECTOR, Selectors.ATTATCHMENT_MENU).click()           
            driver.find_element(By.CSS_SELECTOR, Selectors.INPUT_CONTACTS).click()

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, Selectors.POPUP)))

            for contact in contacts:
                search_bar = driver.find_element(By.CSS_SELECTOR, Selectors.SEARCH_BAR)
                search_bar.send_keys(contact)
                sleep(0.5)

                if element_exists(driver, By.CSS_SELECTOR, Selectors.NO_CONTACTS_FOUND):
                    driver.find_element(By.CSS_SELECTOR, Selectors.CLOSE).click()
                    WebDriverWait(driver, 10).until(
                        EC.invisibility_of_element_located((By.CSS_SELECTOR, Selectors.POPUP)))
                    raise ContactNotFoundException(f"The contact {contact} does not exist.")
                
                search_bar.send_keys(Keys.ENTER)

            driver.find_element(By.CSS_SELECTOR, Selectors.SEND_BUTTON).click() # Send the contacts
            driver.find_element(By.CSS_SELECTOR, Selectors.SEND_BUTTON).click() # Confirm the contacts

            WebDriverWait(driver, 10).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, Selectors.POPUP)))

            if not documents and not midias and message:
                self.send(message=message)

        if documents:
            driver.find_element(By.CSS_SELECTOR, Selectors.ATTATCHMENT_MENU).click()
            driver.find_element(By.CSS_SELECTOR, Selectors.INPUT_DOCUMENTS).send_keys("\n".join(documents))
            
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, Selectors.MEDIA_CAPTION)))

            if message:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, Selectors.MEDIA_CAPTION)))
                
                msg_box = driver.find_element(By.CSS_SELECTOR, Selectors.MEDIA_CAPTION)
                send_keys_multiline(msg_box, message)
            
            driver.find_element(By.CSS_SELECTOR, Selectors.SEND_BUTTON).click()

        if midias:
            driver.find_element(By.CSS_SELECTOR, Selectors.ATTATCHMENT_MENU).click()
            driver.find_element(By.CSS_SELECTOR, Selectors.INPUT_MIDIA).send_keys("\n".join(midias))
            
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, Selectors.MEDIA_CAPTION)))

            if not documents and message:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, Selectors.MEDIA_CAPTION)))
                
                msg_box = driver.find_element(By.CSS_SELECTOR, Selectors.MEDIA_CAPTION)
                send_keys_multiline(msg_box, message)
            
            driver.find_element(By.CSS_SELECTOR, Selectors.SEND_BUTTON).click()

    def clear(self, keep_starred: bool = False) -> None:
        """Clears the conversation messages.

        #### Arguments
            * keep_starred (bool, optional): Whether to keep the starred messages or not. Defaults to False.
        """

        if self._whatsapp.current_chat != self.name:
            raise NotSelectedException(f"The chat \"{self.name}\" is not selected.")

        driver = self._whatsapp.driver

        self._open_menu()

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, Selectors.MENU_CLEAR)))

        driver.find_element(By.CSS_SELECTOR, Selectors.MENU_CLEAR).click()

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, Selectors.POPUP_CONFIRM)))

        if keep_starred:            
            driver.find_element(By.CSS_SELECTOR, Selectors.KEEP_STARRED).click()

        driver.find_element(By.CSS_SELECTOR, Selectors.POPUP_CONFIRM).click()

        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, Selectors.POPUP)))

    def mute(self, time: Literal["8 hours", "1 week", "Always"]) -> None:
        """Mutes the conversation notifications.

        #### Arguments
            * time (Literal["8 hours", "1 week", "Always"]): The time to mute the conversation for.
        """

        if self._whatsapp.current_chat != self.name:
            raise NotSelectedException(f"The chat \"{self.name}\" is not selected.")

        if time.lower() not in ["8 hours", "1 week", "always"]:
            raise ValueError("The time must be one of the following: 8 hours, 1 week, Always.")

        if self.is_muted:
            self.unmute()

        driver = self._whatsapp.driver

        self._open_menu()

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, Selectors.MENU_MUTE)))

        driver.find_element(By.CSS_SELECTOR, Selectors.MENU_MUTE).click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, Selectors.MUTE_POPUP)))

        mute_time_options = driver.find_elements(By.CSS_SELECTOR, Selectors.MUTE_TIME_OPTIONS)

        match time.lower():
            case "8 hours":
                mute_time_options[0].click()
            case "1 week":
                mute_time_options[1].click()
            case "always":
                mute_time_options[2].click()

        driver.find_element(By.CSS_SELECTOR, Selectors.MUTE_POPUP_CONFIRM).click()

        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, Selectors.MUTE_POPUP)))

    def unmute(self) -> None:
        """Unmutes the conversation's notifications."""

        if self._whatsapp.current_chat != self.name:
            raise NotSelectedException(f"The chat \"{self.name}\" is not selected.")

        if not self.is_muted:
            return

        driver = self._whatsapp.driver

        self._open_menu()

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, Selectors.MENU_MUTE)))

        driver.find_element(By.CSS_SELECTOR, Selectors.MENU_MUTE).click()

    def pin(self) -> None:
        """Pins the conversation.

        #### Raises
            * MaxPinnedChatsException: If the maximum pinned chats limit is reached.
        """

        if self._whatsapp.current_chat != self.name:
            raise NotSelectedException(f"The chat \"{self.name}\" is not selected.")

        element, is_pinned = self._is_pinned()

        if is_pinned:
            self._whatsapp._clear_search_bar()
            return

        driver = self._whatsapp.driver

        # Click with the right mouse button to open the menu
        ActionChains(driver).context_click(element).perform()

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, Selectors.MENU_PIN)))

        driver.find_element(By.CSS_SELECTOR, Selectors.MENU_PIN).click()

        try:
            WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, Selectors.POPUP)))

            driver.find_element(By.CSS_SELECTOR, Selectors.POPUP_CONFIRM).click()
            self._whatsapp._clear_search_bar()
            raise MaxPinnedChatsException("You can only pin up to 3 chats.")
        except TimeoutException:
            self._whatsapp._clear_search_bar()

    def unpin(self) -> None:
        """Unpins the conversation."""

        if self._whatsapp.current_chat != self.name:
            raise NotSelectedException(f"The chat \"{self.name}\" is not selected.")

        element, is_pinned = self._is_pinned()

        if not is_pinned:
            self._whatsapp._clear_search_bar()
            return

        driver = self._whatsapp.driver

        # Click with the right mouse button to open the menu
        ActionChains(driver).context_click(element).perform()

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, Selectors.MENU_PIN)))

        driver.find_element(By.CSS_SELECTOR, Selectors.MENU_PIN).click()

        self._whatsapp._clear_search_bar()

    def _open_menu(self) -> None:
        """Opens the conversation menu."""

        self._whatsapp.driver.find_element(By.CSS_SELECTOR, Selectors.CONVERSATION_MENU).click()

    def _is_pinned(self) -> Tuple[WebElement, bool]:
        """Checks if the conversation is pinned but does not clear the search."""

        driver = self._whatsapp.driver
        self._whatsapp._search_chat(self.name)

        # Get all the search results
        result = driver.find_elements(By.CSS_SELECTOR, Selectors.SEARCH_RESULT)
                                      
        # Get all the transform values from style attribute
        elements = {element: element.value_of_css_property("transform") for element in result}

        # get the translate Y value from the transform value
        translate_y = {element: float(transfrom.split(", ")[5].strip(")")) for element, transfrom in elements.items()}

        # get the element with the lowest translate Y value
        element: WebElement = min(translate_y, key=translate_y.get)

        return element, element_exists(element, By.CSS_SELECTOR, Selectors.PIN_ICON)