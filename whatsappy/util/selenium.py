from __future__ import annotations

from time import sleep

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotInteractableException

def find_element_if_exists(driver: WebDriver, *args, **kargs) -> WebElement:
    try:
        return driver.find_element(*args, **kargs)
    except NoSuchElementException:
        return None

def element_exists(driver: WebDriver, *args, **kargs) -> bool:
    return find_element_if_exists(driver, *args, **kargs) is not None

def click_until_interactable(element: WebElement, timeout: int = 10) -> None:
    for _ in range(timeout * 10):
        try:
            element.click()
            break
        except ElementNotInteractableException:
            sleep(0.1)

def send_keys_multiline(element: WebElement, text: str) -> None:
    for line in text.splitlines():
        element.send_keys(line)
        element.send_keys(Keys.SHIFT, Keys.ENTER)

def send_keys_slowly(element: WebElement, text: str, delay: float = 0.05) -> None:
    for char in text:
        element.send_keys(char)
        sleep(delay)

def send_shortcut(driver: WebDriver, *shortcut: str) -> None:
    actions = ActionChains(driver)

    for key in shortcut[:-1]:
        actions.key_down(key)
    actions.send_keys(shortcut[-1])
    actions.perform()

    actions.reset_actions()
    
    for key in shortcut[:-1]:
        actions.key_up(key)
    actions.perform()