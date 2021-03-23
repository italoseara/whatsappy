from .tool import error_log
import traceback

def get_recent_chats(self):
    """Returns a list of all recent chats

    Returns:
        List: All the recent chats
    """
    
    try:
        array = self.driver.execute_script('''
        let asd = document.querySelectorAll('._2Z4DV');
        let newArray = new Array();
        for (var i = 0; i < asd.length; i++){
            newArray.push(asd[i].querySelector('.N2dUK').textContent);
        };

        return newArray;
        ''')

        return array
    except:
        error_log(traceback.format_exc())


def get_pinned_chats(self):
    """Returns a list of all pinned chats

    Returns:
        List: All the pinned chats
    """

    try:
        array = self.driver.execute_script('''
        let pin = document.querySelectorAll('._3EhXO');
        let newArray = new Array();
        for (var i = 0; i < pin.length; i++) {
            newArray.push(pin[i].parentNode.parentNode.parentNode.parentNode.querySelector('._3Dr46').textContent)
        }

        return newArray
        ''')

        return array
    except:
        error_log(traceback.format_exc())