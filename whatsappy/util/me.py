from __future__ import annotations

import requests
from dataclasses import dataclass
from PIL.JpegImagePlugin import JpegImageFile
from PIL import Image

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from . import send_shortcut, Selectors, element_exists
from .. import whatsapp

@dataclass(init=False)
class Me:
    """Utility class for the user's profile. Should not be initialized directly, use `whatsappy.Whatsapp.me` instead."""

    name: str
    about: str
    profile_picture: JpegImageFile

    def __init__(self, _whatsapp: whatsapp.Whatsapp) -> None:
        driver = _whatsapp.driver
        
        send_shortcut(driver, Keys.CONTROL, Keys.ALT, "p")
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, Selectors.MY_PROFILE_TEXT)))

        info = driver.find_elements(By.CSS_SELECTOR, Selectors.MY_PROFILE_TEXT)

        self.name = info[0].text
        self.about = info[1].text if len(info) > 1 else None

        if element_exists(driver, By.CSS_SELECTOR, Selectors.MY_PROFILE_DEFAULT_PIC):
            self.profile_picture = None
        else:
            pfp_url = driver.find_element(By.CSS_SELECTOR, Selectors.MY_PROFILE_PIC).get_attribute("src")
            self.profile_picture = Image.open(requests.get(pfp_url, stream=True).raw)

        ActionChains(driver).send_keys(Keys.ESCAPE).perform()
