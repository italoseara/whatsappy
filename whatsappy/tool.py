from rich.console import Console

console = Console()

def element_exists(self, xpath: str):
    """Verify if the element exists"""

    return self.driver.execute_script(
        f'return !!document.evaluate(\'{xpath}\', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;'
    )


def is_admin(self):
    """Verify if the user is an admin"""

    return element_exists(self,
        '//*[@id="app"]/div[1]/div[1]/div[2]/div[3]/span/div[1]/span/div[1]/div/section/div[5]/div[2]/div[2]'
    )


def close_info(self):
    """Closes group info"""

    self.driver.find_element_by_xpath(
        '//*[@id="app"]/div[1]/div[1]/div[2]/div[3]/span/div[1]/span/div[1]/header/div/div[1]/button'
    ).click()