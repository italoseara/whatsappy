import os
import re
import cv2
import shelve
from time import sleep
from selenium import webdriver
from os import getlogin, mkdir
from webdriver_manager.chrome import ChromeDriverManager

os.environ["WDM_LOG_LEVEL"] = "0"


def get_qrcode(driver, timeout):

    for _ in range(timeout//5):
        qr_code = driver.find_element_by_css_selector(".landing-main")

        qr_code.screenshot("qrcode.png")

        img = cv2.imread("qrcode.png", 1)

        cv2.imshow("Scan the QRCode to login", img)
        cv2.waitKey(5000)
        cv2.destroyAllWindows()

        try:
            driver.find_element_by_css_selector(
                "div.SgIJV > div > label > div > div._2_1wd.copyable-text.selectable-text"
            )
            break
        except:
            pass


def login(self, visible: bool = False, timeout: int = 60):
    """Logs in whatsapp and shows the QRCode if necessary

    Args:
        visible (bool, optional): Shows the process. Defaults to False.
        timeout (int, optional): Limit time to login in seconds. Defalts to 60
    """

    usr_path = (
        f"C:\\Users\\{getlogin()}\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
    )
    try:
        self.mydata = shelve.open("data/data")
    except:
        mkdir("data")
        self.mydata = shelve.open("data/data")

    try:
        print(f'Logging as: {self.mydata["user_agent"]}')
        get_user_agent = False
    except:
        get_user_agent = True

    options = webdriver.ChromeOptions()
    if not get_user_agent:
        options.add_argument(f"--user-data-dir={usr_path}")
        options.add_argument(f"--user-agent={self.mydata['user_agent']}")
    options.add_argument("--start-maximized")
    options.add_argument("--hide-scrollbars")
    options.add_argument("--disable-gpu")
    options.add_argument("--log-level=OFF")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    if not visible:
        options.add_argument("--headless")

    self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    self.driver.get("https://web.whatsapp.com")

    if get_user_agent:
        self.mydata["user_agent"] = self.driver.execute_script(
            "return navigator.userAgent"
        )
        self.mydata.close()

    logged = False
    for _ in range(timeout):
        try:
            self.driver.find_element_by_css_selector(
                "div.SgIJV > div > label > div > div._2_1wd.copyable-text.selectable-text"
            )
            break

        except:
            if not visible:
                try:
                    self.driver.find_element_by_css_selector(".landing-main")

                    get_qrcode(self.driver, timeout)
                    break

                except:
                    sleep(1)
            
            else:
                sleep(1)


    self.driver.implicitly_wait(60)
    self.driver.find_element_by_css_selector(
        "div.SgIJV > div > label > div > div._2_1wd.copyable-text.selectable-text"
    )

    logged = True

    if logged or visible:
        print("Logged")
    else:
        self.close()
        raise Exception("Error trying to login, try again")

    sleep(2)


def close(self):
    """Exit the whatsapp"""

    self.driver.close()