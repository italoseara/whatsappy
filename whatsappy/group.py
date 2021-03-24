from time import sleep
from selenium.webdriver.common.keys import Keys
from .tool import error_log
import traceback

def change_group_description(self, description: str):
    """Changes the group description

    Args:
        description (str): New group description
    """

    try:

        self.driver.find_element_by_css_selector(
            '#main > header > div._2uaUb > div.z4t2k > div > span').click()

        sleep(1)

        try:
            self.driver.find_element_by_css_selector(
                '#app > div > div > div.Akuo4 > div._1Flk2._3xysY > span > div > span > div > div > section > div._3ZEdX._3hiFt._82zXh > div._3NATg > div > div > span._2zDdK > div')

        except:
            print('You are not a group admin!')
            return

        self.driver.find_element_by_css_selector(
            '#app > div > div > div.Akuo4 > div._1Flk2._3xysY > span > div > span > div > div > section > div._3ZEdX._3hiFt._82zXh > div._3NATg > div > div > span._2zDdK > div').click()

        description_dom = self.driver.find_element_by_css_selector(
            '#app > div > div > div.Akuo4 > div._1Flk2._3xysY > span > div > span > div > div > section > div._3ZEdX._3hiFt._82zXh > div._3NATg > div > div._3rhi1 > div > div._2_1wd.copyable-text.selectable-text')

        description_dom.clear()

        if description.find('\n'):
            for line in description.split('\n'):
                description_dom.send_keys(line)
                description_dom.send_keys(Keys.SHIFT + Keys.ENTER)
            description_dom.send_keys(Keys.ENTER)

        else:
            description_dom.send_keys(description)
            
    except:
        error_log(traceback.format_exc())
    
    try:
        self.driver.find_element_by_css_selector('#app > div > div > div.Akuo4 > div._1Flk2._3xysY > span > div > span > div > header > div > div._215wZ > button').click()
    except:
        pass


def change_group_name(self, name: str):
    """Changes the group name

    Args:
        name (str): New group name
    """

    try:

        self.driver.find_element_by_css_selector(
            '#main > header > div._2uaUb > div.z4t2k > div > span').click()

        sleep(1)

        try:
            self.driver.find_element_by_css_selector(
                '#app > div > div > div.Akuo4 > div._1Flk2._3xysY > span > div > span > div > div > section > div._3ZEdX._3hiFt._82zXh > div._3NATg > div > div > span._2zDdK > div')

        except:
            print('You are not a group admin!')
            return

        self.driver.find_element_by_class_name('_1JAUF').click()

        self.driver.find_element_by_css_selector(
            '#app > div > div > div.Akuo4 > div._1Flk2._3xysY > span > div > span > div > div > section > div._3ZEdX._3hiFt.bRenh > div._2O6GW._3Ss_B._1lemF._3Ihuv > div._3rhi1.e1K_H._1nQew > span._2zDdK > div').click()

        group_name_dom = self.driver.find_element_by_css_selector(
            '#app > div > div > div.Akuo4 > div._1Flk2._3xysY > span > div > span > div > div > section > div._3ZEdX._3hiFt.bRenh > div._2O6GW._3Ss_B._1lemF._1fB8E._3Ihuv > div._3rhi1 > div > div._2_1wd.copyable-text.selectable-text')

        group_name_dom.clear()
        group_name_dom.send_keys(name + Keys.ENTER)

    except:
        error_log(traceback.format_exc())
    
    try:
        self.driver.find_element_by_css_selector('#app > div > div > div.Akuo4 > div._1Flk2._3xysY > span > div > span > div > header > div > div._215wZ > button').click()
    except:
        pass


def leave_group(self):
    """Leaves the group you are"""

    self.driver.find_element_by_css_selector(
        '#main > header > div._2uaUb > div.z4t2k > div > span').click()

    self.driver.find_element_by_css_selector(
        '#app > div > div > div.Akuo4 > div._1Flk2._3xysY > span > div > span > div > div > section > div:nth-child(6) > div').click()

    self.driver.find_element_by_css_selector(
        '#app > div > span:nth-child(2) > div > div > div > div > div > div > div._1uJw_ > div._1dwBj._3xWLK').click()