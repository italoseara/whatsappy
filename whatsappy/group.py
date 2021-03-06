from time import sleep
from selenium.webdriver.common.keys import Keys
from os import path
from .tool import error_log
import traceback


def change_group_description(self, description: str):
    """Changes the group description

    Args:
        description (str): New group description
    """

    try:

        self.driver.find_element_by_css_selector("div.z4t2k > div > span").click()

        sleep(1)

        try:
            self.driver.find_element_by_css_selector("span._2zDdK > div")

        except:
            print("You are not a group admin!")
            return

        self.driver.find_element_by_css_selector("span._2zDdK > div").click()

        description_dom = self.driver.find_element_by_css_selector(
            "div._2_1wd.copyable-text.selectable-text"
        )

        description_dom.clear()

        if description.find("\n"):
            for line in description.split("\n"):
                description_dom.send_keys(line)
                description_dom.send_keys(Keys.SHIFT + Keys.ENTER)
            description_dom.send_keys(Keys.ENTER)

        else:
            description_dom.send_keys(description)

    except:
        error_log(traceback.format_exc())

    try:
        self.driver.find_element_by_css_selector("div._215wZ > button").click()
    except:
        pass


def change_group_name(self, name: str):
    """Changes the group name

    Args:
        name (str): New group name
    """

    try:

        self.driver.find_element_by_css_selector("div.z4t2k > div > span").click()

        sleep(1)

        try:
            self.driver.find_element_by_css_selector("span._2zDdK > div")

        except:
            print("You are not a group admin!")
            return

        self.driver.find_element_by_class_name("_1JAUF").click()

        self.driver.find_element_by_css_selector("span._2zDdK > div").click()

        group_name_dom = self.driver.find_element_by_css_selector(
            "div._2_1wd.copyable-text.selectable-text"
        )

        group_name_dom.clear()
        group_name_dom.send_keys(name + Keys.ENTER)

    except:
        error_log(traceback.format_exc())

    try:
        self.driver.find_element_by_css_selector("div._215wZ > button").click()
    except:
        pass


def change_group_pfp(self, file_path: str):

    try:

        if not path.isabs(file_path):
            raise Exception("The file path is not absolute")

        self.driver.find_element_by_css_selector("div.z4t2k > div > span").click()

        sleep(1)

        try:
            self.driver.find_element_by_css_selector("span._2zDdK > div")

        except:
            print("You are not a group admin!")
            return

        self.driver.find_element_by_css_selector(
            "div._3ZEdX._3hiFt.bRenh > div.bnO5E > div > input[type=file]"
        ).send_keys(file_path)

        sleep(1)

        self.driver.execute_script(
            'document.querySelector("div.OMoBQ._3WNg8._3wXwX.copyable-area > div > div._1y7hs > span > div > div").click()'
        )

    except:
        error_log(traceback.format_exc())

    try:
        self.driver.find_element_by_css_selector("div._215wZ > button").click()

    except:
        pass


def leave_group(self):
    """Leaves the group you are"""

    self.driver.find_element_by_css_selector("div.z4t2k > div > span").click()

    self.driver.find_element_by_css_selector(
        "div._1Flk2._3xysY > span > div > span > div > div > section > div:nth-child(6) > div"
    ).click()

    self.driver.find_element_by_css_selector("div._1dwBj._3xWLK").click()
