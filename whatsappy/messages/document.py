from dataclasses import dataclass, field
from typing import List

from selenium.webdriver.remote.webelement import WebElement

from .. import whatsapp

@dataclass(init=False)
class Document:
    """Utility class for documents. Should not be initialized directly, use `whatsappy.Whatsapp.open` instead."""

    name: str = None
    size: str = None
    type: str = None

    def __init__(self, _whatsapp: whatsapp.Whatsapp, _element: WebElement) -> None:
        raise NotImplementedError("This method is not implemented yet.")
    
    def download(self, path: str = None) -> None:
        """Downloads the document.

        Args:
            path (str, optional): The path to download the document to. Defaults to None.
        """

        raise NotImplementedError("This method is not implemented yet.")
