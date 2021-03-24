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
            '#main > header > div._2uaUb > div.z4t2k > div > span').click()

        try:
            self.driver.find_element_by_css_selector(
                '#app > div > div > div.Akuo4 > div._1Flk2._3xysY > span > div > span > div > div > section > div._3ZEdX._3hiFt._82zXh > div._3NATg > div > div > span._2zDdK > div'
            )

        except:
            print('You are not a group admin!')
            
        self.driver.find_element_by_css_selector(
            '#app > div > div > div.Akuo4 > div._1Flk2._3xysY > span > div > span > div > div > section > div:nth-child(5) > div:nth-child(2) > div.TbtXF'
        ).click()

        self.driver.find_element_by_css_selector(
            '#app > div > span:nth-child(2) > div > span > div > div > div > div > div > div > div:nth-child(2) > div > label > div > div._2_1wd.copyable-text.selectable-text'
        ).send_keys(contact_name)
        
        sleep(0.5)
        
        self.driver.find_element_by_css_selector(
            '#app > div > span:nth-child(2) > div > span > div > div > div > div > div > div > div:nth-child(2) > div > label > div > div._2_1wd.copyable-text.selectable-text'
        ).send_keys(Keys.ENTER)
            
        sleep(0.5)

        self.driver.find_element_by_css_selector(
            '#app > div > span:nth-child(2) > div > span > div > div > div > div > div > div > span._3IGMG > div > div > div'
        ).click()

        self.driver.find_element_by_css_selector(
            '#app > div > span:nth-child(2) > div > span > div > div > div > div > div > div._1uJw_ > div._1dwBj._3xWLK'
        ).click()

    except:
        error_log(traceback.format_exc())
    
    try:
        self.driver.find_element_by_css_selector(
            '#app > div > div > div.Akuo4 > div._1Flk2._3xysY > span > div > span > div > header > div > div._215wZ > button'
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
            '#main > header > div._2uaUb > div.z4t2k > div > span').click()

        try:
            self.driver.find_element_by_css_selector(
                '#app > div > div > div.Akuo4 > div._1Flk2._3xysY > span > div > span > div > div > section > div._3ZEdX._3hiFt._82zXh > div._3NATg > div > div > span._2zDdK > div'
            )

        except:
            print('You are not a group admin!')
            return

        self.driver.find_element_by_css_selector(
            '#app > div > div > div.Akuo4 > div._1Flk2._3xysY > span > div > span > div > div > section > div:nth-child(5) > div.-ZdaK > div > div > div._3TVPy'
        ).click()

        sleep(0.5)

        self.driver.find_element_by_css_selector(
            '#app > div > span:nth-child(2) > div > div > div > div > div > div > div > div:nth-child(2) > div > label > div > div._2_1wd.copyable-text.selectable-text'
        ).send_keys(participant_name)

        sleep(0.5)
        
        self.driver.find_element_by_css_selector(
            '#app > div > span:nth-child(2) > div > div > div > div > div > div > div > div._1C2Q3._36Jt6 > div:nth-child(1) > div > div > div > div > div'
        ).click()

        sleep(0.5)

        self.driver.find_element_by_css_selector(
            '#app > div > span:nth-child(4) > div > ul > li:nth-child(2)'
        ).click()

        self.driver.find_element_by_css_selector(
            '#app > div > span:nth-child(2) > div > div > div > div > div > div > div > header > div > div._215wZ > button'
        ).click()
    
    except:
        error_log(traceback.format_exc())
    
    try:
        self.driver.find_element_by_css_selector(
            '#app > div > div > div.Akuo4 > div._1Flk2._3xysY > span > div > span > div > header > div > div._215wZ > button'
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
            '#main > header > div._2uaUb > div.z4t2k > div > span'
        ).click()

        try:
            self.driver.find_element_by_css_selector(
                '#app > div > div > div.Akuo4 > div._1Flk2._3xysY > span > div > span > div > div > section > div._3ZEdX._3hiFt._82zXh > div._3NATg > div > div > span._2zDdK > div'
            )

        except:
            print('You are not a group admin!')
            return

        self.driver.find_element_by_css_selector(
            '#app > div > div > div.Akuo4 > div._1Flk2._3xysY > span > div > span > div > div > section > div:nth-child(5) > div.-ZdaK > div > div > div._3TVPy'
        ).click()

        sleep(0.5)

        self.driver.find_element_by_css_selector(
            '#app > div > span:nth-child(2) > div > div > div > div > div > div > div > div:nth-child(2) > div > label > div > div._2_1wd.copyable-text.selectable-text'
        ).send_keys(participant_name)

        sleep(0.5)
        
        self.driver.find_element_by_css_selector(
            '#app > div > span:nth-child(2) > div > div > div > div > div > div > div > div._1C2Q3._36Jt6 > div:nth-child(1) > div > div > div > div > div'
        ).click()

        sleep(0.5)

        self.driver.find_element_by_css_selector(
            '#app > div > span:nth-child(4) > div > ul > li:nth-child(1)'
        ).click()

        self.driver.find_element_by_css_selector(
            '#app > div > span:nth-child(2) > div > div > div > div > div > div > div > header > div > div._215wZ > button'
        ).click()
    
    except:
        error_log(traceback.format_exc())
    
    try:
        self.driver.find_element_by_css_selector(
            '#app > div > div > div.Akuo4 > div._1Flk2._3xysY > span > div > span > div > header > div > div._215wZ > button'
        ).click()
    except:
        pass