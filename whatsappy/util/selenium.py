from __future__ import annotations

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver

def find_element_if_exists(driver: WebDriver, *args, **kargs) -> WebElement:
    try:
        return driver.find_element(*args, **kargs)
    except NoSuchElementException:
        return None

def element_exists(driver: WebDriver, *args, **kargs) -> bool:
    return find_element_if_exists(driver, *args, **kargs) is not None