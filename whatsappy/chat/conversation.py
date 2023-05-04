from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import List, Literal

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .. import whatsapp
from ..util import *

@dataclass(init=False)
class Conversation:
    """Utility class for chats and groups. Should not be initialized directly, use `whatsappy.Whatsapp.open` instead."""
    
    _whatsapp: whatsapp.Whatsapp = field(repr=False)

    def __init__(self, _whatsapp: whatsapp.Whatsapp) -> None:
        self._whatsapp = _whatsapp

    @property
    def starred_messages(self) -> List[str]:
        """Returns a list of starred messages in the chat."""

        raise NotImplementedError("This method is not implemented yet.")
    
    def send(self, 
             message: str = None, 
             attatchments: List[str] = None, 
             type: Literal["auto", "document", "midia", "contact"] = "auto"
        ) -> None:
        """Sends a message to the chat.

        #### Arguments
            * message (str, optional): The message to send. Defaults to None.
            * attatchments (List[Any], optional): The attatchments to send. Defaults to None.
            * type (Literal["auto", "document", "midia", "contact"], optional): The type of the attatchments. Defaults to "auto".
            If the type is specified, all the attatchments must be of the same type.
        """

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
            elif not os.path.isfile(attatchment):
                raise FileNotFoundError(f"The file {attatchment} does not exist.")

        attatchment_types = {attatchment: type if type != "auto" else get_attachment_type(attatchment) for attatchment in attatchments}

        documents = [attatchment for attatchment, type in attatchment_types.items() if type == "document"]
        midias = [attatchment for attatchment, type in attatchment_types.items() if type == "midia"]
        contacts = [attatchment for attatchment, type in attatchment_types.items() if type == "contact"]

        if contacts:
            raise NotImplementedError("Sending contacts is not implemented yet.")

        if documents:
            driver.find_element(By.CSS_SELECTOR, Selectors.ATTATCHMENT_MENU).click()
            driver.find_element(By.CSS_SELECTOR, Selectors.INPUT_DOCUMENTS).send_keys("\n".join(documents))
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, Selectors.MEDIA_CAPTION)))

            if message:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, Selectors.MEDIA_CAPTION)))
                msg_box = driver.find_element(By.CSS_SELECTOR, Selectors.MEDIA_CAPTION)
                send_keys_multiline(msg_box, message)
            
            driver.find_element(By.CSS_SELECTOR, Selectors.SEND_BUTTON).click()

        if midias:
            driver.find_element(By.CSS_SELECTOR, Selectors.ATTATCHMENT_MENU).click()
            driver.find_element(By.CSS_SELECTOR, Selectors.INPUT_MIDIA).send_keys("\n".join(midias))
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, Selectors.MEDIA_CAPTION)))

            if not documents and message:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, Selectors.MEDIA_CAPTION)))
                msg_box = driver.find_element(By.CSS_SELECTOR, Selectors.MEDIA_CAPTION)
                send_keys_multiline(msg_box, message)
            
            driver.find_element(By.CSS_SELECTOR, Selectors.SEND_BUTTON).click()

    def mute(self, time: Literal["8 hours", "1 week", "Always"]) -> None:
        """Mutes the chat notifications.

        #### Arguments
            * time (Literal["8 hours", "1 week", "Always"]): The time to mute the chat for.
        """

        raise NotImplementedError("This method is not implemented yet.")

    def unmute(self) -> None:
        """Unmutes the chat notifications."""

        raise NotImplementedError("This method is not implemented yet.")

    def archive(self) -> None:
        """Archives the chat."""

        raise NotImplementedError("This method is not implemented yet.")

    def block(self) -> None:
        """Blocks the chat."""

        raise NotImplementedError("This method is not implemented yet.")

    def unblock(self) -> None:
        """Unblocks the chat."""

        raise NotImplementedError("This method is not implemented yet.")

    def delete(self) -> None:
        """Deletes the chat."""

        raise NotImplementedError("This method is not implemented yet.")

    def pin(self) -> None:
        """Pins the chat."""

        raise NotImplementedError("This method is not implemented yet.")
