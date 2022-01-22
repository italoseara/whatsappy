import os
import shelve
import colorama
import platform
from qrcode import QRCode
from time import sleep, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

from .error import LoginError
from .tool import console


os.environ["WDM_LOG_LEVEL"] = "0"


def _get_qrcode(driver, timeout: int, before: int) -> None:

    colorama.init()

    update_qr = ''

    while ((time() - before) < timeout) if timeout else True:
        
        qr_element = driver.find_element(By.XPATH, "//canvas/..")

        qr_data = qr_element.get_attribute("data-ref")

        if qr_data and qr_data != update_qr:
            update_qr = qr_data

            console.clear()
            qr = QRCode(version=1, border=2)
            qr.add_data(qr_data)
            qr.make()
            qr.print_ascii(invert=True)
            
            console.print("Scan the QRCode with your phone")

        sleep(1)


def login(self, visible: bool = True, timeout: int = 0) -> None:
    """Logs in whatsapp and shows the QRCode if necessary

    Args:
        visible (bool, optional): Shows the process. Defaults to False.
        timeout (int, optional): Limit time to login in seconds. Defaults to 0
    """

    os_path = {
        "Windows": rf"{os.path.expanduser('~')}/AppData/Local/Google/Chrome/User Data/Default",   # Windows
        "Linux": rf"{os.path.expanduser('~')}/.config/google-chrome/default",                     # Linux
        "Darwin": rf"{os.path.expanduser('~')}/Library/Application Support/Google/Chrome/Default" # Mac OS
    }

    usr_path = os_path[platform.system()] 

    if not os.path.isdir("data"):
        os.mkdir("data")

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

    before = time()
    while ((time() - before) < timeout) if timeout else True:
        try:
            self.driver.find_element(By.ID, "side")
            break
        
        except NoSuchElementException:
            if not visible:
                try:
                    self.driver.find_element(By.CLASS_NAME, "landing-main")
                    _get_qrcode(self.driver, timeout, before)
                    
                except NoSuchElementException:
                    pass
    else:
        self.close()
        raise LoginError("Failed when trying to log into whatsapp (Took too long to respond)")

    console.print("Successfully logged in")

def close(self) -> None:
    """Exit whatsapp"""

    self.driver.close()
