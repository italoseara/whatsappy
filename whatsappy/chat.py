import re
import shutil
from os import path
from send2trash import send2trash
from selenium.webdriver.common.keys import Keys

from .message import *

_last = ""


def last_message(self):
    """Gets the last message from the chat

    Returns:
        Class: Last message
    """

    type = self.driver.execute_script("""
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

    last_msg = self.driver.execute_script(
        'return [...document.querySelectorAll(".message-in")].slice(-1)[0];')

    classes = {
        "Text": Text,
        "Audio": Audio,
        "Video": Video,
        "Image": Image,
        "Sticker": Sticker,
        "AudioFile": Audio,
        "Document": Document,
        "Location" : Location,
        "ContactCard": ContactCard,
        "LiveLocation": LiveLocation,
    }
    
    if type == "AudioFile":
        return classes[type](_element=last_msg, isrecorded=True, _whatsapp=self)

    return classes[type](_element=last_msg, _whatsapp=self)


def new_message(self):
    """Returns True for a new message

    Returns:
        Bool: New message
    """

    global _last

    message = self.last_message()
    if _last == "":
        _last = message

    if message != _last:
        _last = message
        return True

    else:
        return False


def send(self, message: str) -> None:
    """Sends a message

    Args:
        message (str): The message you want to send or a file path
    """

    if path.isabs(message):
        _send_file(self, file_path=message)
        return None

    chat = self.driver.find_element_by_xpath(
        '//*[@id="main"]/footer/div[1]/div[2]/div/div[1]/div/div[2]'
    )

    if message.find("\n"):
        for line in message.split("\n"):
            chat.send_keys(line)
            chat.send_keys(Keys.SHIFT + Keys.ENTER)
        chat.send_keys(Keys.ENTER)
    else:
        chat.send_keys(message)


def _send_file(self, file_path: str) -> None:
    """Sends a file

    Args:
        file_path (str, absolute path): The file of the path you want to send
    """

    regex = re.compile(r"(\w+\.(\w+))")
    file_name = file_path.split("\\")[-1]
    isZip = False

    if regex.findall(file_name):
        if regex.findall(file_name)[0] in ["png", "jpg", "mp4", "3gpp"]:
            type = 1
        else:
            type = 3

    else:
        shutil.make_archive(file_name, "zip", file_name)

        file_path = path.abspath(file_name + ".zip")
        isZip = True

        type = 3

    self.driver.find_element_by_xpath(
        '//*[@id="main"]/footer/div[1]/div[1]/div[2]/div/div/span'
    ).click()

    img_box = self.driver.find_element_by_xpath(
        f'//*[@id="main"]/footer/div[1]/div[1]/div[2]/div/span/div[1]/div/ul/li[{type}]/button/input'
    )

    img_box.send_keys(file_path)

    while True:
        try:
            self.driver.find_element_by_xpath(
                '//*[@id="app"]/div[1]/div[1]/div[2]/div[2]/span/div[1]/span/div[1]/div/div[2]/div/div[2]/div[2]/div/div'
            ).click()
            break
        except: 
            pass

    if isZip:
        send2trash(file_name + ".zip")
