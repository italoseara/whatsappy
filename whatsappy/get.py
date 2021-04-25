from .tool import error_log
from time import sleep
import traceback


def get_recent_chats(self):
    """Returns a list of all recent chats

    Returns:
        List: All the recent chats
    """

    try:
        array = self.driver.execute_script(
            """
        let asd = document.querySelectorAll('._2Z4DV');
        let newArray = new Array();
        for (var i = 0; i < asd.length; i++){
            newArray.push(asd[i].querySelector('.N2dUK').textContent);
        };

        return newArray;
        """
        )

        return array
    except:
        error_log(traceback.format_exc())


def get_pinned_chats(self):
    """Returns a list of all pinned chats

    Returns:
        List: All the pinned chats
    """

    try:
        array = self.driver.execute_script(
            """
        let pin = document.querySelectorAll('._3EhXO');
        let newArray = new Array();
        for (var i = 0; i < pin.length; i++) {
            newArray.push(pin[i].parentNode.parentNode.parentNode.parentNode.querySelector('._3Dr46').textContent)
        }

        return newArray
        """
        )

        return array
    except:
        error_log(traceback.format_exc())


def get_group_invite_link(self):
    """Returns group invite link

    Returns:
        str: Group invite link
    """

    try:

        self.driver.find_element_by_css_selector(
            "#main > header > div._2uaUb > div.z4t2k > div > span"
        ).click()

        sleep(1)

        try:
            self.driver.find_element_by_css_selector("span._2zDdK > div")

        except:
            print("You are not a group admin!")
            return

        self.driver.find_element_by_css_selector(
            "div._1Flk2._3xysY > span > div > span > div > div > section > div:nth-child(5) > div:nth-child(3)"
        ).click()

        sleep(1)

        group_link = self.driver.find_element_by_css_selector(
            "#group-invite-link-anchor"
        ).text

        self.driver.find_element_by_css_selector("div._215wZ > button").click()

        sleep(1)

        try:
            self.driver.find_element_by_css_selector("div._215wZ > button").click()
        except:
            pass

        return group_link

    except:
        error_log(traceback.format_exc())