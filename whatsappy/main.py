import re
import os
import shutil
import shelve
import colorama
import platform
from typing import Any, List
from inspect import stack
from qrcode import QRCode
from time import sleep, time
from mimetypes import guess_type
from send2trash import send2trash
from dataclasses import dataclass, field

from webdriver_manager.chrome import ChromeDriverManager

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, JavascriptException

from .message import *
from .tool import console
from .error import LoginError


os.environ["WDM_LOG_LEVEL"] = "0"


class Whatsapp:

    def _get_qrcode(self, timeout: int, before: int) -> None:

        colorama.init()

        update_qr = ''

        while ((time() - before) < timeout) if timeout else True:
            
            qr_element = self._driver.find_element(By.XPATH, "//canvas/..")

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

        self._driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        self._driver.get("https://web.whatsapp.com")

        before = time()
        while ((time() - before) < timeout) if timeout else True:
            try:
                self._driver.find_element(By.ID, "side")
                break
            
            except NoSuchElementException:
                if not visible:
                    try:
                        self._driver.find_element(By.CLASS_NAME, "landing-main")
                        self._get_qrcode(timeout, before)
                        
                    except NoSuchElementException:
                        pass
        else:
            self.close()
            raise LoginError("Failed when trying to log into whatsapp (Took too long to respond)")

        console.print("Successfully logged in")

    def close(self) -> None:
        """Exit whatsapp"""

        self._driver.close()

    def chat(self, name: str) -> None:

        self._Chat._open_chat(self, name)

        info = self._driver.find_element(By.CSS_SELECTOR, "section")
        
        return (
            self.Group(self, name) 
            if info.find_elements(By.CSS_SELECTOR, "span[dir=auto].copyable-text button") 
            else self.Contact(self, name))

    def new_group(self, name: str, contacts: list) -> None:
        number_regex = re.compile(r"^\+?[0-9]{10,15}$")
        
        self._driver.find_element(By.CSS_SELECTOR, "span[data-testid=chat]").click()
        self._driver.find_element(By.CSS_SELECTOR, "div[data-testid=cell-frame-container]").click() 
        sleep(.5)
        
        # Search for the contact
        text_box = self._driver.find_element(By.CSS_SELECTOR, "input")
        
        not_saved = []
        for contact in contacts:
            if number_regex.match(contact.replace(" ", "").replace("-", "")):
                not_saved.append(contact.replace(" ", "").replace("-", ""))
                continue
            
            text_box.clear()
            text_box.send_keys(contact)
            sleep(.5)
            
            # Verify if the contact exists
            search_box = self._driver.find_element(By.XPATH, "//header/..")
            found = search_box.find_elements(By.CSS_SELECTOR, "[data-testid=cell-frame-container]")
            
            if not len(found):
                raise ValueError(f'Contact not found: "{contact}"')
            
            # Select the contact
            text_box.send_keys(Keys.ENTER) 
            sleep(.5)

        if len(not_saved) == len(contacts):
            raise ValueError("You need to provide at least one added contact")

        self._driver.find_element(By.CSS_SELECTOR, "span[data-testid=arrow-forward]").click()
        self._driver.find_element(By.CSS_SELECTOR, "[role=textbox]").send_keys(name)
        self._driver.find_element(By.CSS_SELECTOR, "span[data-testid=checkmark-medium]").click()
        sleep(1.5)

        # If the person can only be added by invite link
        if self._driver.find_elements(By.CSS_SELECTOR, "div[data-animate-modal-popup=true]"):
            self._driver.find_elements(By.CSS_SELECTOR, "div[role=button]")[1].click()
            sleep(.5)
            self._driver.find_element(By.CSS_SELECTOR, "div[role=button]").click()

        sleep(.5)

        group = self.Group(self, name)

        for contact in not_saved:
            self._driver.get(f"https://web.whatsapp.com/send?phone={contact}&text={group.invite_link}")
            while True:
                try:
                    self._driver.find_element(By.ID, "side")
                    sleep(1)
                    break
                except NoSuchElementException:
                    pass

            text_box = self._driver.find_elements(By.CSS_SELECTOR, "div[role=textbox]")[1]
            text_box.send_keys(Keys.ENTER)
            group._open_chat(group.name)

        return group

    @property
    def pinned_chats(self) -> None:
        raise NotImplementedError("Not implemented yet")

    @property
    def recent_chats(self) -> None:
        raise NotImplementedError("Not implemented yet")

    @dataclass
    class _Chat:

        _driver: Any = field(repr=False, default=None)

        def _open_chat(self, name: str = None) -> None:
            """Open a chat

            Args:
                name (str): The name of the chat you want to open
            """

            name = name or self.name

            if len(self._driver.find_elements(By.CSS_SELECTOR, "header")) == 3 and\
                self._driver.find_elements(By.CSS_SELECTOR, f"span[title={name}]"):
                return

            number_regex = re.compile(r"^\+?[0-9]{10,15}$")
            if number_regex.match(name.replace(" ", "").replace("-", "")):
                self._driver.get(f"https://web.whatsapp.com/send?phone={name.replace(' ', '').replace('-', '')}")
                while True:
                    try:
                        self._driver.find_element(By.ID, "side")
                        sleep(1)
                        break
                    except NoSuchElementException:
                        pass
            else:
                self._driver.find_element(By.CSS_SELECTOR, "#side div[role=textbox]").send_keys(name + Keys.ENTER)
                
            self._driver.find_element(By.CSS_SELECTOR, "#main > header > div").click()

            section = self._driver.find_element(By.CSS_SELECTOR, "section")
            if len(section.find_elements(By.CSS_SELECTOR, "button[type=button]")) > 1:
                section.find_elements(By.CSS_SELECTOR, "button[type=button]")[1].click()
            sleep(1.5)

        def send(self, message: str = "", file: str = "") -> None:
            """Sends a message

            Args:
                message (str): The message you want to send
                file (str): The path of the file you want to send
            """

            def send_message(message: str, text_box: Any) -> None:
                if "\n" in message:
                    for line in message.split("\n"):
                        text_box.send_keys(line)
                        text_box.send_keys(Keys.SHIFT + Keys.ENTER)
                else:
                    text_box.send_keys(message)

            self._open_chat()

            text_box = self._driver.find_elements(By.CSS_SELECTOR, "div[role=textbox]")[-1]
            
            if file:
                if os.path.isfile(file) or os.path.isdir(file):
                    file = os.path.abspath(file)
                    file_name = os.path.basename(file)
                    file_type = "document"

                    if (
                        "image" in guess_type(file)[0] or
                        guess_type(file)[0] in ["video/mp4", "video/3gpp", "video/quicktime"]
                    ):
                        file_type = "image"
                        
                    elif os.path.isdir(file):
                        shutil.make_archive(file_name, "zip", file_name)
                        file = os.path.abspath(file_name + ".zip")

                    self._driver.find_element(By.CSS_SELECTOR, "span[data-testid=clip]").click()
                    attach = self._driver.find_element(By.XPATH, f"//span[@data-testid='attach-{file_type}']/../input")
                    attach.send_keys(file)
                    sleep(.5)

                    while True:
                        if send_btn := self._driver.find_elements(By.CSS_SELECTOR, "span[data-testid=send]"):
                            send_btn = send_btn[0]
                            if file_type == "image":
                                text_box = self._driver.find_element(By.CSS_SELECTOR, "div[role=textbox]")
                                send_message(message, text_box)
                                send_btn.click()
                                return
                            else:
                                send_btn.click()
                                break

                    if ".zip" in file:
                        send2trash(file)
                else:
                    raise FileNotFoundError(f"File {file} not found")
                
            send_message(message, text_box)
            text_box.send_keys(Keys.ENTER)

        @property
        def last_message(self) -> Any:
            """Gets the last message from the chat

            Returns:
                Class: Last message
            """

            self._open_chat()
            
            try:
                type = self._driver.execute_script("""
                    var lastMsg = [...document.querySelectorAll(".message-in")].slice(-1)[0];

                    if (
                        lastMsg.querySelector("button > div:nth-child(2) > div > div:nth-child(3)")
                    ) return "Document";

                    else if (
                        lastMsg.querySelector("div > div > div:nth-child(3)") &&
                        lastMsg.querySelector("div > div > div:nth-child(3)").style.backgroundImage
                    ) return "Video";

                    else if (
                        lastMsg.querySelector("div > button > span") &&
                        lastMsg.querySelector("div > button > span").dataset.testid == "audio-play"
                    )
                        if (
                            lastMsg.querySelector("div:nth-child(2) > div:nth-child(2) > span") &&
                            lastMsg.querySelector("div:nth-child(2) > div:nth-child(2) > span")
                            .dataset.testid == "forward-chat"
                        ) return "AudioFile";
                        else return "Audio";

                        else if (
                            lastMsg.querySelector(
                                `div > div > div > div:nth-child(2) > div > div > div:nth-child(2) > div[role="button"]`
                            ) &&
                            !lastMsg.querySelector('span[data-testid="logo-youtube"]')
                        ) return "ContactCard";

                    else if (
                        lastMsg.querySelector("div > span > span > svg")
                    ) return "LiveLocation";

                    else if (
                        lastMsg.querySelector("a > img")
                    ) return "Location";

                    else if (
                        lastMsg.querySelector("img")
                    )
                        if (lastMsg.querySelector("img").classList.contains('copyable-text') ||
                            lastMsg.querySelector('span[data-testid="logo-youtube"]'))
                            return "Text"
                        else if (
                            lastMsg.querySelector("div:nth-child(2) > div:nth-child(2) > span") &&
                            lastMsg.querySelector("div").querySelector("span").dataset.testid ==
                            "tail-in"
                        ) return "Image";
                        else return "Sticker";

                    else return "Text";
                """)
            except JavascriptException:
                return None
            
            last_msg = self._driver.execute_script(
                'return [...document.querySelectorAll(".message-in")].slice(-1)[0];')

            classes = {
                "Text": Text,
                "Audio": Audio,
                "Video": Video,
                "Image": Image,
                "Sticker": Sticker,
                "Document": Document,
                "Location" : Location,
                "ContactCard": ContactCard,
                "LiveLocation": LiveLocation,
                "AudioFile": lambda **kwargs: Audio(**kwargs, isrecorded=True),
            }

            return classes[type](chat=self, _element=last_msg, _whatsapp=self)

    @dataclass
    class Contact(_Chat):

        name: str = None
        number: str = None
        about: str = None
        profile_picture: str = None

        def __init__(self, parent, name) -> None:
            """Initialize a contact"""

            self._driver = parent._driver
            self._open_chat(name)

            info = self._driver.find_element(By.CSS_SELECTOR, "section")
            contact_info = info.find_elements(By.CSS_SELECTOR, "span[dir=auto].copyable-text")
            
            self.name = contact_info[0].text
            self.number = contact_info[1].text
            self.about = contact_info[2].get_property("title")

            img_section = self._driver.find_element(By.CSS_SELECTOR, "section > div")
            if img_element := img_section.find_elements(By.CSS_SELECTOR, "img"):
                self.profile_picture = img_element[0].get_attribute("src")

            number_regex = re.compile(r"^\+?[0-9]{10,15}$")
            if number_regex.match(self.name.replace(" ", "").replace("-", "")):
                self.name, self.number = (
                    self.number.replace("~", ""), 
                    self.name.replace(" ", "").replace("-", "")
                )

    @dataclass
    class Group(_Chat):

        name: str = None
        description: str = None
        profile_picture: str = None
        invite_link: str = None
        admin: bool = False
        _left: bool = field(repr=False, default=False)

        def __init__(self, parent, name) -> None:
            """Initializes a group"""

            self._driver = parent._driver
            self._open_chat(name)
            
            info = self._driver.find_element(By.CSS_SELECTOR, "section")

            self.name = info.find_element(By.CSS_SELECTOR, "div[role=textbox]").text
            self.description = info.find_elements(By.CSS_SELECTOR, "span[dir=auto].copyable-text")[1].text

            img_section = self._driver.find_element(By.CSS_SELECTOR, "section > div")
            if img_element := img_section.find_elements(By.CSS_SELECTOR, "img"):
                self.profile_picture = img_element[0].get_attribute("src")

            name = info.find_elements(By.CSS_SELECTOR, "div[role=gridcell]")[-2]
            self.admin = "\n" in name.text

            if self.admin:
                self._driver.find_elements(By.CSS_SELECTOR, "div[data-testid=cell-frame-container]")[1].click()
                sleep(.5)
                self.invite_link = self._driver.find_element(By.CSS_SELECTOR, "#group-invite-link-anchor").text
                
                self._driver.find_element(By.CSS_SELECTOR, "span[data-testid=back]").click()
                sleep(1)

        def __setattr__(self, __name: str, __value: Any) -> None:

            if stack()[1][3] == "__init__":
                return super().__setattr__(__name, __value)
            
            self._open_chat()

            info = self._driver.find_element(By.CSS_SELECTOR, "section")
            edit_btns = info.find_elements(By.XPATH, "//span[@data-testid='pencil']/..")

            if not edit_btns:
                raise PermissionError("You don't have permission to edit this group")

            sleep(.5)
            match __name:
                
                case "name":
                    edit_btns[0].find_element(By.XPATH, "../..").click()
                    edit_btns[0].click()

                    edit_name = info.find_element(By.CSS_SELECTOR, "div[role=textbox]")
                    edit_name.clear()
                    edit_name.send_keys(__value + Keys.ENTER)

                case "description":
                    edit_btns[1].find_element(By.XPATH, "../..").click()
                    edit_btns[1].click()

                    edit_description = info.find_elements(By.CSS_SELECTOR, "div[role=textbox]")[1]
                    edit_description.clear()
                    
                    if "\n" in __value:
                        for line in __value.split("\n"):
                            edit_description.send_keys(line)
                            edit_description.send_keys(Keys.SHIFT + Keys.ENTER)
                    else:
                        edit_description.send_keys(__value)

                    edit_description.send_keys(Keys.ENTER)

                case "profile_picture":
                    raise NotImplementedError("Not implemented yet")

                case _:
                    raise AttributeError(f"{__name} is not a valid attribute")
                
            return super().__setattr__(__name, __value)

        def _participant_options(self, contacts, function) -> None:
            """Local function to go to the participants options and execute a function"""
            
            self._open_chat()

            if self._left:
                raise PermissionError("You have left the group")
            
            # Verify if you are admin
            if not self.admin:
                raise PermissionError("You are not a group admin!")

            for contact in contacts:
                # Click on the search icon
                self._driver.find_element(By.CSS_SELECTOR, "span[data-testid=search]").click()

                # Search for the contact
                text_box = self._driver.find_element(By.CSS_SELECTOR, "[role=textbox]")
                text_box.clear()
                text_box.send_keys(contact)
                sleep(.3)

                # Verify if the contact exists
                search_box = self._driver.find_element(By.XPATH, "//header/..")
                contacts_found = search_box.find_elements(By.CSS_SELECTOR, "div[data-testid=cell-frame-container]")
                
                if not len(contacts_found):
                    raise ValueError(f'Contact not found: "{contact}"')

                # Verify if the contact is an admin
                contact_name = search_box.find_element(By.CSS_SELECTOR, "div[role=gridcell]")
                contact_admin = "\n" in contact_name.text

                contacts_found[-1].click()
                options = self._driver.find_elements(By.CSS_SELECTOR, "li > div:nth-child(1)")
                sleep(.5)
                
                function(options, contact, contact_admin)

            self._driver.find_element(By.CSS_SELECTOR, "span[data-testid=x]").click()

        def add(self, contacts: List[str]) -> None:
            """Adds new participants to the group

            Args:
                contacts (list): A list of contacts that you want to add to the group
            """
            number_regex = re.compile(r"^\+?[0-9]{10,15}$")

            self._open_chat()

            if self._left:
                raise PermissionError("You have left the group")

            # Verify if you are admin
            if not self.admin:
                raise PermissionError("You are not a group admin!")

            # Click to add a participant
            self._driver.find_element(By.CSS_SELECTOR, "[data-testid=cell-frame-container]").click() 
            
            # Search for the contact
            text_box = self._driver.find_element(By.CSS_SELECTOR, "[role=textbox]")
            
            not_saved = []
            for contact in contacts:
                if number_regex.match(contact.replace(" ", "").replace("-", "")):
                    not_saved.append(contact.replace(" ", "").replace("-", ""))
                    continue
                
                text_box.clear()
                text_box.send_keys(contact)
                sleep(.5)
                
                # Verify if the contact exists
                search_box = self._driver.find_element(By.XPATH, "//header/..")
                found = search_box.find_elements(By.CSS_SELECTOR, "[data-testid=cell-frame-container]")
                
                if not len(found):
                    raise ValueError(f'Contact not found: "{contact}"')
                
                # Select the contact
                text_box.send_keys(Keys.ENTER) 
                sleep(.5)

            for contact in not_saved:
                self._driver.get(f"https://web.whatsapp.com/send?phone={contact}&text={self.invite_link}")
                while True:
                    try:
                        self._driver.find_element(By.ID, "side")
                        sleep(1)
                        break
                    except NoSuchElementException:
                        pass

                text_box = self._driver.find_elements(By.CSS_SELECTOR, "div[role=textbox]")[1]
                text_box.send_keys(Keys.ENTER)
                self._open_chat()

            # Click to add them
            self._driver.find_element(By.CSS_SELECTOR, "span[data-testid=checkmark-medium]").click()
            
            # Confirm the addition
            self._driver.find_elements(By.CSS_SELECTOR, "div[role=button]")[1].click()
            sleep(1.5)

            # If the person can only be added by invite link
            if self._driver.find_elements(By.CSS_SELECTOR, "div[data-animate-modal-popup=true]"):
                self._driver.find_elements(By.CSS_SELECTOR, "div[role=button]")[1].click()
                sleep(.5)
                self._driver.find_element(By.CSS_SELECTOR, "div[role=button]").click()

            sleep(.5)

        def remove(self, contacts: List[str]) -> None:
            """Removes participants from the group

            Args:
                contacts (list): A list of contacts that you want to remove from the group
            """

            def _remove(options, contact, contact_admin) -> None:
                
                # NOTE: In python, 0 == False and 1 == True, 
                # so, if the user is admin it will click on the first option
                # else, it will click on the second option (because of the "not" operator)
                options[not contact_admin].click()

            self._participant_options(contacts, _remove)

        def promote(self, contacts: List[str]) -> None:
            """Promotes participants to admin

            Args:
                contacts (list): A list of contacts that you want to promote to admin
            """
            
            def _promote(options, contact, contact_admin) -> None:
                if not contact_admin:
                    options[0].click()
                else:
                    raise ValueError(f'"{contact}" is already an admin!')

            self._participant_options(contacts, _promote)

        def demote(self, contacts: List[str]) -> None:
            """Demotes participants to member

            Args:
                contact (str): The contact that you want to demote to member
            """
            
            def _demote(options, contact, contact_admin) -> None:
                if contact_admin:
                    options[1].click()
                else:
                    raise ValueError(f'"{contact}" is not an admin!')

            self._participant_options(contacts, _demote)

        def leave(self) -> None:
            """Leaves the group"""

            if self._left:
                raise PermissionError("You have already left the group")
            
            info = self._driver.find_element(By.CSS_SELECTOR, "section")
            info.find_elements(By.CSS_SELECTOR, "div[role=button]")[-2].click()
            popup = self._driver.find_element(By.CSS_SELECTOR, "div[data-animate-modal-popup='true']")
            popup.find_elements(By.CSS_SELECTOR, "div[role=button]")[1].click()

            self._left = True
