from dataclasses import dataclass, field
from email.policy import default
from PIL import Image as PILImage
from datetime import datetime
from typing import Any, List
from pathlib import Path
from io import BytesIO
from time import sleep
import mimetypes
import re

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from .tool import to_soup, parse_message, blob_to_bytes


@dataclass
class Text:

    @dataclass
    class Quote:
        text: str
        author: str

    text: str = ""
    author: str = None
    quote: Quote = None
    time: datetime = None
    forwarded: bool = False
    _chat: Any = field(repr=False, default=None)
    _element: WebElement = field(repr=False, default=None)

    def __post_init__(self):

        self._driver = self._element.parent
        
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

            self.quote = self.Quote(
                text=parse_message(quoted), 
                author=quoted.parent.parent.span.text
            )
        
        if soup.find("span", attrs={"data-testid": "forwarded"}):
            self.forwarded = True

    def _get_options(self):

        self._driver.execute_script("""
            var event = new MouseEvent('mouseover', {
                'view': window,
                'bubbles': true,
                'cancelable': true
            });

            var element = arguments[0].querySelector("div");

            element.dispatchEvent(event);
        """, self._element)

        self._element.find_elements(By.CSS_SELECTOR, 'span[data-testid="down-context"]').click()

        return self._driver.find_elements(By.CSS_SELECTOR, "ul > div > li")

    def forward(self, contacts: List[str]) -> None:
        """Forwards the selected message to all listed contacts

        Keep in mind that the message won't be avaliable anymore,
        because it will leave the current chat

        Args:
            contacts (List[str]): A list with contacts name
        """

        options = self._get_options()
        options[-3 if (self._chat.__class__.__name__ == "Contact") else -4].click()
        
        self._driver.find_element(By.CSS_SELECTOR, "span[data-testid=forward]").click()

        search_box = self._driver.find_element(By.CSS_SELECTOR, 'div[role="textbox"]')

        for contact in contacts:
            search_box.send_keys(contact)
            search_box.send_keys(Keys.ENTER)
        
        self._driver.find_element(By.CSS_SELECTOR, 'div[role="button"]').click()

        self._chat._open_chat()

    def reply(self, message: str = "", file: str = "") -> None:
        """Replies to the selected message

        Args:
            message (str): The message you want to send
        """

        _actionChains = ActionChains(self._element.parent)

        _actionChains.double_click(self._element).perform()
        self._chat.send(message, file)

    def reply_privately(self, message: str = "", file: str = "") -> None:
        """Sends a message message privatly to the selected message

        Args:
            message (str): The message you want to send
        """

        if self._chat.__class__.__name__ == "Contact":
            raise PermissionError("You cannot reply privately in a private chat")

        options = self._get_options()
        options[1].click()
        sleep(.1)
        
        self._chat.send(message, file)
        self._chat._open_chat()

    def delete(self) -> None:
        """Deletes the selected message"""

        options = self._get_options()
        options[-1 if (self._chat.__class__.__name__ == "Contact") else -2].click()
        
        self._driver.find_element(By.CSS_SELECTOR, 'div:nth-child(2)[role="button"]').click()

    def star(self) -> None:
        """Stars the selected message"""

        options = self._get_options()
        options[-2 if (self._chat.__class__.__name__ == "Contact") else -3].click()


@dataclass
class Document(Text):

    @dataclass
    class File:
        size: int = 0
        name: str = ""
        mimetype: str = ""
        content: bytes = field(repr=False, default=b"")

    file: File = None

    def __post_init__(self):
        super().__post_init__()
        mimetypes.init()

        soup = to_soup(self._element)
        for span in soup.find_all("span"):
            file_name = span.text
            if Path(file_name).suffix:
                file_type = mimetypes.types_map[Path(file_name).suffix]
                break

        # Download file
        self._element.find_element(By.CSS_SELECTOR, 'button').click()

        file_path = str(Path.home()/"Downloads"/file_name)

        while True:
            if Path(file_path).is_file():
                break

        with open(file_path, "rb") as f:
            file_content = f.read()
            file_size = len(file_content)

        Path(file_path).unlink()
        self.file = self.File(
            name=file_name, 
            mimetype=file_type, 
            size=file_size, 
            content=file_content
        )


@dataclass
class Video(Text):

    length: int = 0

    def __post_init__(self):
        super().__post_init__()
        soup = to_soup(self._element)

        length_str = (
            soup.find("span", attrs={"data-testid": "msg-video"})
            .parent.parent.text
            .split(":")
        )
        self.length = (int(length_str[0]) * 60) + int(length_str[1])
    
    def forward(self):
        if self.forwarded:
            raise PermissionError("You cannot forward a forwarded Video")

        super().forward()


@dataclass
class Audio(Text):

    @dataclass
    class File:
        size: int = 0
        length: int = 0
        content: bytes = field(repr=False, default=b"")

    file: File = None
    isrecorded: bool = False

    def __post_init__(self):
        super().__post_init__()
        soup = to_soup(self._element)

        length_str = soup.find("div", attrs={"aria-hidden": "true"}).text.split(":")
        length = (int(length_str[0]) * 60) + int(length_str[1])

        #! Not working anymore
        # url = soup.find("audio")["src"]
        # content = blob_to_bytes(self._element.parent, url)
        content = None

        size = len(content) if content else 0

        self.file = self.File(size=size, length=length, content=content)


@dataclass
class ContactCard(Text):

    @dataclass
    class Contact:
        name: str = ""
        numbers: List[str] = field(default_factory=list)

    contacts: List[Contact] = field(default_factory=list)

    def __post_init__(self):
        super().__post_init__()
        self._element.find_element(By.CSS_SELECTOR, 'div[role="button"]').click()

        soup = to_soup(self._driver.find_element(By.CSS_SELECTOR, "body"))
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
        self._driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Close"]').click()


@dataclass
class Location(Text):

    coords: tuple = ()
    link: str = ""

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

    def __post_init__(self):
        soup = to_soup(self._element)
        driver_find = self._element.parent.find_element_by_css_selector
        
        if active := soup.find("span", attrs={"data-testid": "live-location-active-android"}):

            regex = re.compile("(\d{1,2}\:\d{2}\s?(?:AM|PM|am|pm))")
            until_str = active.parent.parent.text
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

    def forward(self):
        raise PermissionError("You cannot forward a LiveLocation")


@dataclass
class Image(Text):

    @dataclass
    class File:
        size: int = 0
        resolution: tuple = ()
        content: bytes = field(repr=False, default=b"")

    file: File = None

    def __post_init__(self):
        super().__post_init__()
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
