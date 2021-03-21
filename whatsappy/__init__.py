import os
import re
import shelve
from selenium import webdriver
from os import getlogin, mkdir
from webdriver_manager.chrome import ChromeDriverManager

from .cmds.actions import add_to_group, remove_from_group, make_group_admin
from .cmds.chat import select_chat, last_message, new_message, send, reply, send_file
from .cmds.get import get_pinned_chats, get_recent_chats
from .cmds.group import change_group_description, change_group_name, leave_group

os.environ['WDM_LOG_LEVEL'] = '0'

class Whatsapp:

    def add_to_group(self, contact_name: str):
        """Add a new participant to the group

        Args:
            contact_name (str): The contact name of who you want to add
        """

        add_to_group(self, contact_name)

    def remove_from_group(self, participant_name: str):
        """Removes a participant from the group

        Args:
            participant_name (str): The contact name or number of who you want to remove
        """
        
        remove_from_group(self, participant_name)

    def make_group_admin(self, participant_name: str):
        """
        Makes someone a group admin

        Args:
            participant_name (str): [The contact name or number of who you want to make admin
        """
        
        make_group_admin(self, participant_name)
    
    def select_chat(self, chat_name: str):
        """
        Go to the selected chat

        Args:
            chat_name (str): Contact/Group name
        """
        
        select_chat(self, chat_name)
    
    def last_message(self):
        """
        Gets the last message from the chat

        Returns:
            Class: Last message
        """
        
        last_message(self)
    
    def new_message(self):
        """
        Returns True for a new message

        Returns:
            Bool: New message
        """
        
        new_message(self)
   
    def send(self, message: str):
        """
        Sends a message

        Args:
            message (str): The message you want to send
        """
        
        send(self, message)
    
    def reply(self, message: str):
        """
        Replies to the last message

        Args:
            message (str): The message you want to send
        """
        
        reply(self, message)
    
    def send_file(self, file_path: str):
        """Sends a file

        Args:
            file_path (str/absolute path): The file of the path you want to send
        """
        
        send_file(self, file_path)
    
    def get_pinned_chats(self):
        """
        Returns a list of all pinned chats

        Returns:
            List: All the pinned chats
        """
        
        get_pinned_chats(self)
    
    def get_recent_chats(self):
        """
        Returns a list of all recent chats

        Returns:
            List: All the recent chats
        """
        
        get_recent_chats(self)

    def change_group_description(self, description: str):
        """
        Changes the group description

        Args:
            description (str): New group description
        """
        
        change_group_description(self, description)
    
    def change_group_name(self, name: str):
        """
        Changes the group name

        Args:
            name (str): New group name
        """
        
        change_group_name(self, name)
    
    def leave_group(self):
        """Leaves the group you are"""
        
        leave_group(self)

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
        exit()

    # TODO: get group invite link

    # TODO: invite by number

    # TODO: private answer

    # TODO: Get group info (maybe turn it into a class)

    # TODO: Decent error message

    # TODO: Create group

whatsapp = Whatsapp()