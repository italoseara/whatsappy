from __future__ import annotations

import requests
from dataclasses import dataclass
from PIL.JpegImagePlugin import JpegImageFile
from PIL import Image
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait

from . import send_shortcut, Selectors, element_exists
from .. import whatsapp

@dataclass(init=False)
class Me:
    name: str
    about: str
    profile_picture: JpegImageFile

    def __init__(self, _whatsapp: whatsapp.Whatsapp) -> None:
        driver = _whatsapp.driver
        
        send_shortcut(driver, Keys.CONTROL, Keys.ALT, "p")
        WebDriverWait(driver, 10).until(lambda driver: not _whatsapp._is_animating())
        sleep(0.1) # Wait for the about to load

        info = driver.find_elements(By.CSS_SELECTOR, Selectors.MY_PROFILE_TEXT)

        self.name = info[0].text
        self.about = info[1].text if len(info) > 1 else None

        if element_exists(driver, By.CSS_SELECTOR, Selectors.MY_PROFILE_DEFAULT_PIC):
            self.profile_picture = None
        else:
            pfp_url = driver.find_element(By.CSS_SELECTOR, Selectors.MY_PROFILE_PIC).get_attribute("src")
            self.profile_picture = Image.open(requests.get(pfp_url, stream=True).raw)

        ActionChains(driver).send_keys(Keys.ESCAPE).perform()

    def set_name(self, name: str) -> None:
        raise NotImplementedError("This method is not implemented yet.")

    def set_about(self, about: str) -> None:
        raise NotImplementedError("This method is not implemented yet.")

    def set_profile_picture(self, path: str) -> None:
        raise NotImplementedError("This method is not implemented yet.")