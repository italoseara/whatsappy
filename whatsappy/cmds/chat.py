import re
import shutil
from os import path
from time import sleep
from send2trash import send2trash
from selenium.webdriver.common.keys import Keys


last = ''

class Message:

    def __init__(self, author, content, time, date):
        self.author  = author
        self.time    = time
        self.date    = date
        self.content = content
    
    def __str__(self):
        return f'Author: {self.author}\nTime: {self.time}\nDate: {self.date}\nContent: {self.content}'


def select_chat(self, chat_name: str):
    """Go to the selected chat

    Args:
        chat_name (str): Contact/Group name
    """

    self.driver.find_element_by_css_selector(
        '#side > div.SgIJV > div > label > div > div._2_1wd.copyable-text.selectable-text').send_keys(chat_name)
    self.driver.find_element_by_css_selector(
        '#side > div.SgIJV > div > label > div > div._2_1wd.copyable-text.selectable-text').send_keys(Keys.ENTER)


def last_message(self):
    """Gets the last message from the chat
    
    Returns:
        Class: Last message
    """

    global Message

    try:
        info = self.driver.execute_script('''
            var a = document.querySelectorAll(".GDTQm.message-in");
            return a[a.length - 1].querySelector('.copyable-text').dataset.prePlainText;
        ''')
            
        content = self.driver.execute_script('''
            var a = document.querySelectorAll(".GDTQm.message-in");
            return a[a.length - 1].querySelector('.copyable-text').innerText;
        ''')

        time = re.compile(r'(\d+:\d+(\s)?(AM|PM)?)').findall(info)[0][0]
        date = re.compile(r'(\d+/\d+/\d+)').findall(info)[0]
        author = re.compile(r'] (.*):').findall(info)[0]

        return Message(author=author, content=content, time=time, date=date)
    except:
        print('Something gone wrong')


def new_message(self):
    """Returns True for a new message

    Returns:
        Bool: New message
    """

    global last
        
    try:
        message = self.last_message()
        if last == '': last = message.content

        if message.content != last:
            last = message.content
            return True
            
        else:
            return False
    except:
        pass


def send(self, message: str):
    """Sends a message

    Args:
        message (str): The message you want to send
    """

    try:
        chat = self.driver.find_element_by_css_selector(
            '#main > footer > div.vR1LG._3wXwX.copyable-area > div._2A8P4 > div > div._2_1wd.copyable-text.selectable-text')

        if message.find('\n'):
            for line in message.split('\n'):
                chat.send_keys(line)
                chat.send_keys(Keys.SHIFT + Keys.ENTER)
            chat.send_keys(Keys.ENTER)
        else:
            chat.send_keys(message)
    except:
        print('Something gone wrong')

    
def reply(self, message: str):
    """Replies to the last message

    Args:
        message (str): The message you want to send
    """
        
    self.driver.execute_script('''
        var a = document.querySelectorAll('.message-in');
        var elem = a[a.length -1]
        var clickEvent = document.createEvent('MouseEvents');
        clickEvent.initEvent('dblclick', true, true);
        elem.dispatchEvent(clickEvent);
    ''')
    self.send(message)


def send_file(self, file_path: str):
    """Sends a file

    Args:
        file_path (str/absolute path): The file of the path you want to send
    """

    regex = re.compile(r'(\w+\.(\w+))')
    file_name = file_path.split('\\')[-1]
    isZip = False

    if regex.findall(file_name):
        if regex.findall(file_name)[0] in ['png', 'jpg', 'mp4', '3gpp']:
            type = 1
        else:
            type = 3

    else:
        shutil.make_archive(file_name, 'zip', file_name)

        file_path = path.abspath(file_name + '.zip')
        isZip = True

        type = 3

    self.driver.execute_script('''
        document.querySelector("#main > footer > div.vR1LG._3wXwX.copyable-area > div.EBaI7._23e-h > div._2C9f1 > div > div").click()
    ''')

    sleep(0.7)

    img_box = self.driver.find_element_by_css_selector(
        f'#main > footer > div.vR1LG._3wXwX.copyable-area > div.EBaI7._23e-h > div._2C9f1 > div > span > div > div > ul > li:nth-child({type}) > button > input[type=file]')
        
    img_box.send_keys(file_path)

    while True:
        try:
            self.driver.find_element_by_css_selector(
                '#app > div > div > div.Akuo4 > div._1Flk2._1sFTb > span > div > span > div > div > div._36Jt6.tEF8N > span > div > div > span').click()
            break
        except:
            pass

    if isZip:
        send2trash(file_name + '.zip')