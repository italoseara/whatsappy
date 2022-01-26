import base64
from bs4 import BeautifulSoup
from rich.console import Console
from selenium.webdriver.remote.webelement import WebElement

console = Console()

def to_soup(element: WebElement):
    return BeautifulSoup(element.get_attribute("innerHTML"), "html.parser")


def parse_message(element_soup) -> str:

    msg = element_soup

    for emoji in msg.find_all("img"):
        msg = str(msg).replace(str(emoji), str(emoji["alt"]))
    
    if type(msg) == str:
        return BeautifulSoup(msg, "html.parser").text

    return msg.text


def blob_to_bytes(driver, url: str) -> bytes:
    result = driver.execute_async_script("""
        var uri = arguments[0];
        var callback = arguments[1];
        var toBase64 = function(buffer){for(var r,n=new Uint8Array(buffer),t=n.length,a=new Uint8Array(4*Math.ceil(t/3)),i=new Uint8Array(64),o=0,c=0;64>c;++c)i[c]="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".charCodeAt(c);for(c=0;t-t%3>c;c+=3,o+=4)r=n[c]<<16|n[c+1]<<8|n[c+2],a[o]=i[r>>18],a[o+1]=i[r>>12&63],a[o+2]=i[r>>6&63],a[o+3]=i[63&r];return t%3===1?(r=n[t-1],a[o]=i[r>>2],a[o+1]=i[r<<4&63],a[o+2]=61,a[o+3]=61):t%3===2&&(r=(n[t-2]<<8)+n[t-1],a[o]=i[r>>10],a[o+1]=i[r>>4&63],a[o+2]=i[r<<2&63],a[o+3]=61),new TextDecoder("ascii").decode(a)};
        var xhr = new XMLHttpRequest();
        xhr.responseType = 'arraybuffer';
        xhr.onload = function(){ callback(toBase64(xhr.response)) };
        xhr.onerror = function(){ callback(xhr.status) };
        xhr.open('GET', uri);
        xhr.send();
    """, url)

    return base64.b64decode(result)


def get_options(self, driver):

    driver.execute_script("""
        var event = new MouseEvent('mouseover', {
            'view': window,
            'bubbles': true,
            'cancelable': true
        });

        var element = arguments[0].querySelector("div");

        element.dispatchEvent(event);
    """, self._element)

    self._element.find_element_by_css_selector(
        'span[data-testid="down-context"]').click()

    return driver.find_elements_by_css_selector("ul > div > li")