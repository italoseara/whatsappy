import os
import re
import shelve
from selenium import webdriver
from os import getlogin, mkdir
from webdriver_manager.chrome import ChromeDriverManager

os.environ['WDM_LOG_LEVEL'] = '0'

def get_qrcode(self):
    """Opens a new chrome page with the QRCode"""

    usr_path = f"C:\\Users\\{getlogin()}\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
    self.mydata = shelve.open('data/data')

    options = webdriver.ChromeOptions()
    options.add_argument("--log-level=OFF")
    options.add_argument(f'--user-data-dir={usr_path}')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    driver.get('https://web.whatsapp.com')

    self.mydata['user_agent'] = driver.execute_script("return navigator.userAgent;")

    while True:
        try:
            driver.find_element_by_css_selector(
                '#side > div.SgIJV > div > label > div > div._2_1wd.copyable-text.selectable-text')
            break
        except: pass
    driver.close()


def login(self, visible: bool=False):
    """Logs in whatsapp and shows the QRCode if necessary

    Args:
        visible (bool, optional): Shows the process. Defaults to False.
    """

    usr_path = f"C:\\Users\\{getlogin()}\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
    try:
        self.mydata = shelve.open('data/data')
    except:
        mkdir('data')
        self.mydata = shelve.open('data/data')

    try:
        print(f'Logging as: {self.mydata["user_agent"]}')
    except:
        self.get_qrcode()
        
    
    options = webdriver.ChromeOptions()
    options.add_argument(f'--user-data-dir={usr_path}')
    options.add_argument(f"--user-agent={self.mydata['user_agent']}")
    options.add_argument("--start-maximized")
    options.add_argument("--hide-scrollbars")
    options.add_argument("--disable-gpu")
    options.add_argument("--log-level=OFF")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    if not visible:
        options.add_argument("--headless")

    self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    self.driver.get('https://web.whatsapp.com')

    while True:
        try:
            if not visible:
                try: 
                    self.driver.find_element_by_css_selector(
                        '#app > div > div > div.landing-window > div.landing-main > div > div.O1rXL > div > canvas')
                    self.driver.close()
                    self.get_qrcode()
                    self.login(visible=visible)
                    break

                except:
                    try:
                        self.driver.find_element_by_xpath(
                            "//a[@title='Atualize o Google Chrome']")
                        self.driver.close()
                        self.get_qrcode()
                        self.login(visible=visible)
                        break
                    
                    except:
                        self.driver.find_element_by_css_selector(
                            '#side > div.SgIJV > div > label > div > div._2_1wd.copyable-text.selectable-text')
                        print('Logged in')
                        break
            else:
                self.driver.find_element_by_css_selector(
                    '#side > div.SgIJV > div > label > div > div._2_1wd.copyable-text.selectable-text')
                print('Logged in')
                break
        except:
            pass


def exit(self):
    """Exit the whatsapp"""

    self.driver.close()
    quit()