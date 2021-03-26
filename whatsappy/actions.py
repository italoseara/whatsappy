from time import sleep
from selenium.webdriver.common.keys import Keys
from .tool import error_log
import traceback


def add_to_group(self, contact_name: str):
    """Add a new participant to the group

    Args:
        contact_name (str): The contact name of who you want to add
    """

    try:

        self.driver.find_element_by_css_selector(
            "#main > header > div._2uaUb > div.z4t2k > div > span"
        ).click()

        try:
            self.driver.find_element_by_css_selector(
                "#app > div > div > div.Akuo4 > div._1Flk2._3xysY > span > div > span > div > div > section > div._3ZEdX._3hiFt._82zXh > div._3NATg > div > div > span._2zDdK > div"
            )

        except:
            print("You are not a group admin!")

        self.driver.find_element_by_css_selector(
            "#app > div > div > div.Akuo4 > div._1Flk2._3xysY > span > div > span > div > div > section > div:nth-child(5) > div:nth-child(2) > div.TbtXF"
        ).click()

        self.driver.find_element_by_css_selector(
            "#app > div > span:nth-child(2) > div > span > div > div > div > div > div > div > div:nth-child(2) > div > label > div > div._2_1wd.copyable-text.selectable-text"
        ).send_keys(contact_name)

        sleep(0.5)

        self.driver.find_element_by_css_selector(
            "#app > div > span:nth-child(2) > div > span > div > div > div > div > div > div > div:nth-child(2) > div > label > div > div._2_1wd.copyable-text.selectable-text"
        ).send_keys(Keys.ENTER)

        sleep(0.5)

        self.driver.find_element_by_css_selector(
            "#app > div > span:nth-child(2) > div > span > div > div > div > div > div > div > span._3IGMG > div > div > div"
        ).click()

        self.driver.find_element_by_css_selector(
            "#app > div > span:nth-child(2) > div > span > div > div > div > div > div > div._1uJw_ > div._1dwBj._3xWLK"
        ).click()

        sleep(2)

        try:
            self.driver.find_element_by_css_selector(
                "#app > div._3h3LX._34ybp.app-wrapper-web.font-fix.os-win > span:nth-child(2) > div._1XTIr > span > div:nth-child(1) > div > div > div > div > div._1uJw_ > div._1dwBj._3xWLK"
            ).click()
            sleep(0.5)

            self.driver.find_element_by_css_selector(
                "#app > div._3h3LX._34ybp.app-wrapper-web.font-fix.os-win > span:nth-child(2) > div._1XTIr > span > div.overlay._1814Z._3wXwX.copyable-area > div > div > div > div > div > div > span > div"
            ).click()
        except:
            pass

    except:
        error_log(traceback.format_exc())

    try:
        self.driver.find_element_by_css_selector(
            "#app > div > div > div.Akuo4 > div._1Flk2._3xysY > span > div > span > div > header > div > div._215wZ > button"
        ).click()
    except:
        pass


def remove_from_group(self, participant_name: str):
    """Removes a participant from the group

    Args:
        participant_name (str): The contact name or number of who you want to remove
    """

    try:

        self.driver.find_element_by_css_selector(
            "#main > header > div._2uaUb > div.z4t2k > div > span"
        ).click()

        try:
            self.driver.find_element_by_css_selector(
                "#app > div > div > div.Akuo4 > div._1Flk2._3xysY > span > div > span > div > div > section > div._3ZEdX._3hiFt._82zXh > div._3NATg > div > div > span._2zDdK > div"
            )

        except:
            print("You are not a group admin!")
            return

        self.driver.find_element_by_css_selector(
            "#app > div > div > div.Akuo4 > div._1Flk2._3xysY > span > div > span > div > div > section > div:nth-child(5) > div.-ZdaK > div > div > div._3TVPy"
        ).click()

        sleep(0.5)

        self.driver.find_element_by_css_selector(
            "#app > div > span:nth-child(2) > div > div > div > div > div > div > div > div:nth-child(2) > div > label > div > div._2_1wd.copyable-text.selectable-text"
        ).send_keys(participant_name)

        sleep(0.5)

        self.driver.find_element_by_css_selector(
            "#app > div > span:nth-child(2) > div > div > div > div > div > div > div > div._1C2Q3._36Jt6 > div:nth-child(1) > div > div > div > div > div"
        ).click()

        sleep(0.5)

        self.driver.find_element_by_css_selector(
            "#app > div > span:nth-child(4) > div > ul > li:nth-child(2)"
        ).click()

        self.driver.find_element_by_css_selector(
            "#app > div > span:nth-child(2) > div > div > div > div > div > div > div > header > div > div._215wZ > button"
        ).click()

    except:
        error_log(traceback.format_exc())

    try:
        self.driver.find_element_by_css_selector(
            "#app > div > div > div.Akuo4 > div._1Flk2._3xysY > span > div > span > div > header > div > div._215wZ > button"
        ).click()
    except:
        pass


def make_group_admin(self, participant_name: str):
    """Makes someone a group admin

    Args:
        participant_name (str): [The contact name or number of who you want to make admin
    """

    try:

        self.driver.find_element_by_css_selector(
            "#main > header > div._2uaUb > div.z4t2k > div > span"
        ).click()

        try:
            self.driver.find_element_by_css_selector(
                "#app > div > div > div.Akuo4 > div._1Flk2._3xysY > span > div > span > div > div > section > div._3ZEdX._3hiFt._82zXh > div._3NATg > div > div > span._2zDdK > div"
            )

        except:
            print("You are not a group admin!")
            return

        self.driver.find_element_by_css_selector(
            "#app > div > div > div.Akuo4 > div._1Flk2._3xysY > span > div > span > div > div > section > div:nth-child(5) > div.-ZdaK > div > div > div._3TVPy"
        ).click()

        sleep(0.5)

        self.driver.find_element_by_css_selector(
            "#app > div > span:nth-child(2) > div > div > div > div > div > div > div > div:nth-child(2) > div > label > div > div._2_1wd.copyable-text.selectable-text"
        ).send_keys(participant_name)

        sleep(0.5)

        self.driver.find_element_by_css_selector(
            "#app > div > span:nth-child(2) > div > div > div > div > div > div > div > div._1C2Q3._36Jt6 > div:nth-child(1) > div > div > div > div > div"
        ).click()

        sleep(0.5)

        self.driver.find_element_by_css_selector(
            "#app > div > span:nth-child(4) > div > ul > li:nth-child(1)"
        ).click()

        self.driver.find_element_by_css_selector(
            "#app > div > span:nth-child(2) > div > div > div > div > div > div > div > header > div > div._215wZ > button"
        ).click()

    except:
        error_log(traceback.format_exc())

    try:
        self.driver.find_element_by_css_selector(
            "#app > div > div > div.Akuo4 > div._1Flk2._3xysY > span > div > span > div > header > div > div._215wZ > button"
        ).click()
    except:
        pass


def select_chat_by_name(self, chat_name: str):
    """Go to the selected chat by its number

    Args:
        chat_name (str): Contact/Group name
    """

    self.driver.find_element_by_css_selector(
        "#side > div.SgIJV > div > label > div > div._2_1wd.copyable-text.selectable-text"
    ).send_keys(chat_name)

    self.driver.find_element_by_css_selector(
        "#side > div.SgIJV > div > label > div > div._2_1wd.copyable-text.selectable-text"
    ).send_keys(Keys.ENTER)


def select_chat_by_number(self, chat_number: int):
    """Go to the selected chat by its number

    Args:
        chat_number (int): Contact number. Example: 1NPAXXXXXXX
    """

    self.driver.get(f"https://web.whatsapp.com/send?phone={chat_number}")
    sleep(5)


def create_group(self, group_name: str, contacts: list):

    """Create a new whatsapp group

    Args:
        group_name (str): Name of the group
        contacts (list): List of contacts to add into the group
    """

    self.driver.execute_script(
        "document.querySelector('#side > header > div._2XP8p > div > span > div:nth-child(3) > div').click()"
    )

    self.driver.execute_script(
        "document.querySelector('#side > header > div._2XP8p > div > span > div._2n-zq._3zHcq > span > div > ul > li:nth-child(1)').click()"
    )

    for contact in contacts:
        box = self.driver.find_element_by_css_selector(
            "#app > div > div > div.Akuo4 > div._1Flk2._2DPZK > span > div > span > div > div > div._3tEPr > div > div > input"
        )

        box.clear()
        box.send_keys(contact)
        box.send_keys(Keys.ENTER)

    self.driver.execute_script(
        "document.querySelector('#app > div > div > div.Akuo4 > div._1Flk2._2DPZK > span > div > span > div > div > span > div').click()"
    )

    self.driver.find_element_by_css_selector(
        "#app > div > div > div.Akuo4 > div._1Flk2._2DPZK > span > div > span > div > div > div:nth-child(2) > div > div._3rhi1 > div > div._2_1wd.copyable-text.selectable-text"
    ).send_keys(group_name)

    self.driver.execute_script(
        "document.querySelector('#app > div > div > div.Akuo4 > div._1Flk2._2DPZK > span > div > span > div > div > span > div > div').click()"
    )
    sleep(2)

    try:
        self.driver.find_element_by_css_selector(
            "#app > div._3h3LX._34ybp.app-wrapper-web.font-fix.os-win > span:nth-child(2) > div._1XTIr > span > div:nth-child(1) > div > div > div > div > div._1uJw_ > div._1dwBj._3xWLK"
        ).click()
        sleep(0.5)

        self.driver.find_element_by_css_selector(
            "#app > div._3h3LX._34ybp.app-wrapper-web.font-fix.os-win > span:nth-child(2) > div._1XTIr > span > div.overlay._1814Z._3wXwX.copyable-area > div > div > div > div > div > div > span > div"
        ).click()
    except:
        pass
