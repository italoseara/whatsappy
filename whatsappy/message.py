from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
from dataclasses import dataclass, field
from PIL import Image as PILImage
from datetime import datetime
from typing import Any, List
from pathlib import Path
from io import BytesIO
from time import sleep
import mimetypes
import re

from .tool import to_soup, parse_message, blob_to_bytes, get_options
from .error import InvalidActionError


@dataclass
class Message:

    @dataclass
    class Quote:
        text: str
        author: str

    text: str = None
    author: str = None
    quote: Quote = None
    time: datetime = None
    forwarded: bool = False
    _whatsapp: Any = field(repr=False, default=None)
    _element: WebElement = field(repr=False, default=None)

    def __post_init__(self):
        soup = to_soup(self._element)

        if copyable_text := soup.find(class_="copyable-text"):

            msg_metadata = copyable_text["data-pre-plain-text"]
            self.text = parse_message(copyable_text.find(class_="copyable-text").span)
            
            time_msg = re.compile(r"(\d+:\d+(\s)?(AM|PM)?)").findall(msg_metadata)[0][0]
            date_msg = re.compile(r"(\d+/\d+/\d+)").findall(msg_metadata)[0]
            self.author = re.compile(r"] (.*):").findall(msg_metadata)[0]

            self.time = (
                datetime.strptime(f"{date_msg} {time_msg}", "%m/%d/%Y %I:%M %p")
                if ("AM" in time_msg) or ("PM" in time_msg)
                else datetime.strptime(f"{date_msg} {time_msg}", "%d/%m/%Y %H:%M")
            )
        
        if quoted := soup.find(class_="quoted-mention"):

            quoted_text = parse_message(quoted)
            quoted_author = (
                quoted.parent.parent.span.text
            )

            self.quote = self.Quote(text=quoted_text, author=quoted_author)
        
        if soup.find("span", attrs={"data-testid": "forwarded"}):
            self.forwarded = True

    def forward(self, contacts: List[str]):
        """Forwards the selected message to all listed contacts

        Keep in mind that the message won't be avaliable anymore,
        because it will leave the current chat

        Args:
            contacts (List[str]): A list with contacts name
        """

        driver = self._element.parent

        group_name = driver.find_element_by_xpath(
            '//*[@id="main"]/header/div[2]/div'
        ).text

        options = get_options(self, driver)
        
        options[1].click()\
            if len(options) <= 5\
                else options[2].click()
        
        driver.find_elements_by_css_selector(
            "button")[-1].click()

        search_box = driver.find_element_by_css_selector('label > div > div[role="textbox"]')

        for contact in contacts:
            search_box.send_keys(contact)
            sleep(0.1)
            search_box.send_keys(Keys.ENTER)
            sleep(0.1)
        
        driver.find_element_by_css_selector(
            'div[role="button"]').click()

        self._whatsapp.select_chat_by_name(group_name)

    def reply(self, message: str):
        """Replies to the selected message

        Args:
            message (str): The message you want to send
        """

        _actionChains = ActionChains(self._element.parent)

        _actionChains.double_click(self._element).perform()
        self._whatsapp.send(message)

    def reply_privately(self, message: str):
        """Sends a message message privatly to the selected message

        Args:
            message (str): The message you want to send
        """

        driver = self._element.parent

        group_name = driver.find_element_by_xpath(
            '//*[@id="main"]/header/div[2]/div'
        ).text

        options = get_options(self, driver)

        if len(options) <= 5:
            raise InvalidActionError("You cannot reply privately in a private chat")

        options[1].click()
        sleep(0.1)
        
        self._whatsapp.send(message)
        self._whatsapp.select_chat_by_name(group_name)

    def delete(self):
        """Deletes the selected message"""

        driver = self._element.parent
        soup = to_soup(self._element)

        options = get_options(self, driver)

        if soup.find("span", attrs={"data-testid": "media-play"}):
            options[-2].click()
        
        else:
            options[-1].click()\
                if len(options) <= 5\
                    else options[-2].click()
        
        driver.find_element_by_css_selector(
            'div:nth-child(2)[role="button"]').click()

    def star(self):
        """Stars the selected message"""

        driver = self._element.parent
        soup = to_soup(self._element)

        options = get_options(self, driver)

        if soup.find("span", attrs={"data-testid": "media-play"}):
            options[-3].click()
        
        else:
            options[-2].click()\
                if len(options) <= 5\
                    else options[-3].click()


@dataclass
class Text(Message):
    ...


@dataclass
class Document(Message):

    @dataclass
    class File:
        name: str
        type: str
        size: int
        content: bytes = field(repr=False)

    file: File = None

    def __post_init__(self):
        Message.__post_init__(self)
        mimetypes.init()

        soup = to_soup(self._element)
        for span in soup.find_all("span"):
            file_name = span.text
            if Path(file_name).suffix:
                file_type = mimetypes.types_map[Path(file_name).suffix]
                break

        # Download file
        self._element.find_element_by_css_selector('button').click()

        file_path = str(Path.home()/"Downloads"/file_name)

        while True:
            if Path(file_path).is_file():
                break

        with open(file_path, "rb") as f:
            file_content = f.read()
            file_size = len(file_content)

        Path(file_path).unlink()
        self.file = self.File(name=file_name, type=file_type, size=file_size, content=file_content)


@dataclass
class Video(Message):

    length: int = None

    def __post_init__(self):
        Message.__post_init__(self)
        soup = to_soup(self._element)

        length_str = (
            soup.find("span", attrs={"data-testid": "msg-video"})
            .parent.parent.text
            .split(":")
        )
        self.length = (int(length_str[0]) * 60) + int(length_str[1])
    
    def forward(self):
        raise InvalidActionError("You cannot forward a Video")


@dataclass
class Audio(Message):

    @dataclass
    class File:
        size: int
        length: int
        content: bytes = field(repr=False)

    file: File = None
    isrecorded: bool = False

    def __post_init__(self):
        Message.__post_init__(self)
        soup = to_soup(self._element)

        length_str = soup.find("div", attrs={"aria-hidden": "true"}).text.split(":")
        length = (int(length_str[0]) * 60) + int(length_str[1])

        url = soup.find("audio")["src"]
        content = blob_to_bytes(self._element.parent, url)

        size = len(content)

        self.file = self.File(size=size, length=length, content=content)


@dataclass
class ContactCard(Message):

    @dataclass
    class Contact:
        name: str
        numbers: List[str]

        def send_message(message: str) -> None:
            pass

    contacts: List[Contact] = field(default_factory=list)

    def __post_init__(self):
        Message.__post_init__(self)
        self._element.find_element_by_css_selector('div[role="button"]').click()

        driver_find = self._element.parent.find_element_by_css_selector

        soup = to_soup(driver_find("body"))
        contact_elements = [
            contact.parent for contact in soup
            .select(".copyable-area:not(.overlay)")[0]
            .find_all("div", attrs={"data-testid": "cell-frame-container"})
        ]
        
        for contact in contact_elements:

            self.contacts.append( 
                self.Contact(
                    name=contact.find("span", attrs={"dir": "auto"}, class_="copyable-text").text,
                    numbers=[number.text for number in contact.find_all("div", class_="copyable-text")]
                )
            )

        sleep(0.1)
        driver_find('button[aria-label="Close"]').click()


@dataclass
class Location(Message):

    coords: tuple = None
    link: str = None

    def __post_init__(self):
        soup = to_soup(self._element)

        self.link = soup.find("a")["href"]
        self.coords = tuple(
            re.compile("[-]?[\d]+[.][\d]*")
            .findall(self.link)
        )


@dataclass
class LiveLocation(Location):

    until: datetime = None

    def forward(self):
        raise InvalidActionError("You cannot forward a LiveLocation")

    def __post_init__(self):
        soup = to_soup(self._element)
        driver_find = self._element.parent.find_element_by_css_selector
        
        if active := soup.find("span", attrs={"data-testid": "live-location-active-android"}):

            until_str = active.parent.parent.text

            regex = re.compile("(\d{1,2}\:\d{2}\s?(?:AM|PM|am|pm))")

            time_msg = regex.findall(until_str)[0]

            self.until = (
                datetime.strptime(time_msg, "%I:%M %p")
                if ("AM" in time_msg) or ("PM" in time_msg)
                else datetime.strptime(time_msg, "%H:%M")
            )
        

        today = datetime.now()
        self.until.replace(
            year=today.year,
            month=today.month,
            day=today.day
        )

        self._element.find_element_by_css_selector("img")\
            .find_element_by_xpath('..')\
            .click()
        
        while not driver_find("a[rel=noopener]").is_displayed():
            pass

        self.link = (
            driver_find("a[rel=noopener]")
            .get_property("href")
        )
        self.coords = tuple(
            re.compile("[-]?[\d]+[.][\d]*")
            .findall(self.link)
        )
        
        driver_find('button[aria-label="Close"]').click()


@dataclass
class Image(Message):

    @dataclass
    class File:
        size: int
        resolution: tuple
        content: bytes = field(repr=False)

    file: File = None

    def __post_init__(self):
        Message.__post_init__(self)
        soup = to_soup(self._element)

        for img in soup.findAll("img"):
            if "web.whatsapp.com" in img["src"]:
                content = blob_to_bytes(driver=self._element.parent, url=img["src"])
                break

        size = len(content)
        
        image = PILImage.open(BytesIO(content))
        resolution = image.size

        self.file = self.File(size=size, resolution=resolution, content=content)


@dataclass
class Sticker(Image):
    ...
