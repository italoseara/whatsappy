import os
import time
import shelve
import platform
from os import mkdir
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

from . import ascii_qrcode
from .error import LoginError
from .tool import console, terminal_size

os.environ["WDM_LOG_LEVEL"] = "0"


def _get_qrcode(driver, timeout: int, before: int) -> None:

    global rows, columns

    qr_str_old = ''

    min_columns, min_rows = 110, 55
    columns, rows = os.get_terminal_size()

    if rows <= min_rows or columns <= min_columns:
        terminal_size(min_columns, min_rows)

    while (time.time() - before) < timeout:
        
        qr_code = driver.find_element_by_css_selector('.landing-main > div > div:nth-child(2) > div')

        qr_str = qr_code.get_attribute("data-ref")

        if qr_str != qr_str_old:
            qr_str_old = qr_str

            console.clear()
            print(ascii_qrcode.draw(qr_str))
            console.print("Scan the QRCode with your phone")

        time.sleep(1)


def login(self, visible: bool = True, timeout: int = 60) -> None:
    """Logs in whatsapp and shows the QRCode if necessary

    Args:
        visible (bool, optional): Shows the process. Defaults to False.
        timeout (int, optional): Limit time to login in seconds. Defalts to 60
    """

    os_path = {
        "Windows": rf"{os.path.expanduser('~')}/AppData/Local/Google/Chrome/User Data/Default",   # Windows
        "Linux": rf"{os.path.expanduser('~')}/.config/google-chrome/default",                     # Linux
        "Darwin": rf"{os.path.expanduser('~')}/Library/Application Support/Google/Chrome/Default" # Mac OS
    }

    qr_needed = False
    usr_path = os_path[platform.system()] 

    if not os.path.isdir("data"):
        mkdir("data")

    self.mydata = shelve.open("data/data")
    
    if "user_agent" not in self.mydata.keys():

        options = webdriver.ChromeOptions()
        options.add_argument("--hide-scrollbars")
        options.add_argument("--disable-gpu")
        options.add_argument("--log-level=OFF")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

        self.mydata["user_agent"] = driver.execute_script(
            "return navigator.userAgent"
        )

        driver.close()

    options = webdriver.ChromeOptions()
    options.add_argument(f"--user-data-dir={usr_path}")
    options.add_argument(f"--user-agent={self.mydata['user_agent']}")
    options.add_argument("--start-maximized")
    options.add_argument("--hide-scrollbars")
    options.add_argument("--disable-gpu")
    options.add_argument("--log-level=OFF")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    
    self.mydata.close()

    if not visible:
        options.add_argument("--headless")

    self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    self.driver.get("https://web.whatsapp.com")

    before = time.time()
    while (time.time() - before) < timeout:
        
        try:
            self.driver.find_element_by_xpath(
                '//*[@id="side"]/div[1]/div/label/div/div[2]')
            break

        except NoSuchElementException:

            if not visible:
            
                try:
                    self.driver.find_element_by_css_selector(".landing-main")
                    qr_needed = True
                    _get_qrcode(self.driver, timeout, before)

                except (NoSuchElementException, StaleElementReferenceException):
                    pass

    else:
        self.close()
        raise LoginError("Failed when trying to log into whatsapp (Took too long to respond)")

    if qr_needed:
        terminal_size(columns, rows)

    console.log("Successfully logged in")

def close(self) -> None:
    """Exit the whatsapp"""

    self.driver.close()
