import os
from re import S
import shelve
import platform
from os import mkdir
from time import sleep
from . import ascii_qrcode
from .tool import console
from .error import LoginError
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

os.environ["WDM_LOG_LEVEL"] = "0"


def get_qrcode(driver, timeout: int):

    qr_str_old = ''

    min_rows, min_columns = 55, 110
    rows, columns = os.get_terminal_size()

    if rows < min_rows or columns < min_columns:
        os.system(f'mode con: cols={min_columns} lines={min_rows}')

    for _ in range(timeout):
        
        qr_code = driver.find_element_by_css_selector('.landing-main > div > div:nth-child(2) > div')

        qr_str = qr_code.get_attribute("data-ref")

        if qr_str != qr_str_old:
            qr_str_old = qr_str

            console.clear()
            print(ascii_qrcode.draw(qr_str))
            console.print("[bold]Scan the QRCode with your phone")

        try:
            driver.find_element_by_xpath(
                '//*[@id="side"]/div[1]/div/label/div/div[2]')
            
            os.system(f'mode con: cols={columns} lines={rows}')
            break
        except Exception:
            pass

        sleep(1)


def login(self, visible: bool = True, timeout: int = 60):
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

    logged = False
    for _ in range(timeout):
        try:
            self.driver.find_element_by_xpath(
                '//*[@id="side"]/div[1]/div/label/div/div[2]'
            )
            break

        except:
            if not visible:
                try:
                    self.driver.find_element_by_css_selector(".landing-main")          
                    get_qrcode(self.driver, timeout)
                    break

                except Exception:
                    sleep(1)
            
            else:
                sleep(1)


    self.driver.implicitly_wait(60)
    self.driver.find_element_by_xpath(
        '//*[@id="side"]/div[1]/div/label/div/div[2]'
    )

    logged = True

    if logged or visible:
        console.log("Successfully logged in")
    else:
        self.close()
        raise LoginError("Failed when trying to log into whatsapp")


def close(self):
    """Exit the whatsapp"""

    self.driver.close()
