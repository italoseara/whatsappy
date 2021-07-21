import logging
from .tool import *
from time import sleep
from .error import PermissionError
from selenium.webdriver.common.keys import Keys


def add_to_group(self, contact_name: str):
    """Add a new participant to the group

    Args:
        contact_name (str): The contact name of who you want to add
    """

    # Abre as informações do grupo
    self.driver.find_element_by_xpath('//*[@id="main"]/header/div[2]').click()

    # Verifica se você é admin
    if not is_admin(self):
        logging.error("The user is not a group admin")
        raise PermissionError("You are not a group admin!")

    self.driver.find_element_by_xpath(
        '//*[@id="app"]/div[1]/div[1]/div[2]/div[3]/span/div[1]/span/div[1]/div/section/div[5]/div[2]/div[2]'
    ).click() # Clica para adicionar participante

    self.driver.find_element_by_xpath(
        '//*[@id="app"]/div[1]/span[2]/div[1]/span/div[1]/div/div/div/div/div/div[1]/div/label/div/div[2]'
    ).send_keys(contact_name) # Pesquisa o nome do contato

    sleep(0.5) # Espera carregar o contato

    self.driver.find_element_by_xpath(
        '//*[@id="app"]/div[1]/span[2]/div[1]/span/div[1]/div/div/div/div/div/div[1]/div/label/div/div[2]'
    ).send_keys(Keys.ENTER) # Seleciona o contato

    sleep(0.5)

    self.driver.find_element_by_xpath(
        '//*[@id="app"]/div[1]/span[2]/div[1]/span/div[1]/div/div/div/div/div/span[2]/div/div/div'
    ).click() # Clica para adicionar

    self.driver.find_element_by_xpath(
        '//*[@id="app"]/div[1]/span[2]/div[1]/span/div[1]/div/div/div/div/div[2]/div[2]'
    ).click() # Confirma

    sleep(1.5)

    # Caso a pessoa só possa ser convidada via link de convite
    if element_exists(self,
        '//*[@id="app"]/div[1]/span[2]/div[1]/span/div[1]/div/div/div/div/div[2]/div[2]'
    ):

        self.driver.find_element_by_xpath(
            '//*[@id="app"]/div[1]/span[2]/div[1]/span/div[1]/div/div/div/div/div[2]/div[2]'
        ).click()

        sleep(0.5)

        self.driver.find_element_by_xpath(
            '//*[@id="app"]/div[1]/span[2]/div[1]/span/div[1]/div/div/div/div/div/div/span/div'
        ).click()

    sleep(0.5)

    logging.info(f"You added {contact_name} to the group")
    close_info()


def remove_from_group(self, participant_name: str):
    """Removes a participant from the group

    Args:
        participant_name (str): The contact name or number of who you want to remove
    """

    # Abre as informações do grupo
    self.driver.find_element_by_xpath('//*[@id="main"]/header/div[2]').click()

    # Verifica se você é admin
    if not is_admin(self):
        logging.error("The user is not a group admin")
        raise PermissionError("You are not a group admin!")

    self.driver.find_element_by_xpath(
        '//*[@id="app"]/div[1]/div[1]/div[2]/div[3]/span/div[1]/span/div[1]/div/section/div[5]/div[1]/div/div/div[2]'
    ).click() # Clica na lupa de pesquisa

    sleep(0.5)

    self.driver.find_element_by_xpath(
        '//*[@id="app"]/div[1]/span[2]/div[1]/div/div/div/div/div/div/div[1]/div/label/div/div[2]'
    ).send_keys(participant_name) # Busca pelo participante

    sleep(0.5)

    self.driver.find_element_by_xpath(
        '//*[@id="app"]/div[1]/span[2]/div[1]/div[1]/div/div/div/div/div/div[2]/div[1]/div/div/div/div/div/div[2]'
    ).click() # Clica no participante

    sleep(0.5)

    # Verifica se o participante é administrador
    if element_exists(self,
        '//*[@id="app"]/div[1]/span[2]/div[1]/div/div/div/div/div/div/div[2]/div[1]/div/div/div/div/div/div[2]/div[1]/div[2]'
    ):
        
        # Caso sim, clica no primeiro botão
        self.driver.find_element_by_xpath(
            '//*[@id="app"]/div[1]/span[4]/div/ul/div/li[1]/div[1]'
        ).click()
    
    else:
        # Caso não, clica no segundo botão
        self.driver.find_element_by_xpath(
            '//*[@id="app"]/div[1]/span[4]/div/ul/div/li[2]/div[1]'
        ).click()

    self.driver.find_element_by_xpath(
        '//*[@id="app"]/div[1]/span[2]/div[1]/div/div/div/div/div/div/header/div/div[1]/button'
    ).click()

    logging.info(f"You removed {participant_name} from the group")
    close_info()


def make_group_admin(self, participant_name: str):
    """Makes someone a group admin

    Args:
        participant_name (str): The contact name or number of who you want to make admin
    """

    # Abre as informações do grupo
    self.driver.find_element_by_xpath('//*[@id="main"]/header/div[2]').click()

    # Verifica se você é admin
    if not is_admin(self):
        logging.error("The user is not a group admin")
        raise PermissionError("You are not a group admin!")

    self.driver.find_element_by_xpath(
        '//*[@id="app"]/div[1]/div[1]/div[2]/div[3]/span/div[1]/span/div[1]/div/section/div[5]/div[1]/div/div/div[2]'
    ).click() # Clica na lupa de pesquisa

    sleep(0.5)

    self.driver.find_element_by_xpath(
        '//*[@id="app"]/div[1]/span[2]/div[1]/div/div/div/div/div/div/div[1]/div/label/div/div[2]'
    ).send_keys(participant_name) # Busca pelo participante

    sleep(0.5)

    self.driver.find_element_by_xpath(
        '//*[@id="app"]/div[1]/span[2]/div[1]/div[1]/div/div/div/div/div/div[2]/div[1]/div/div/div/div/div/div[2]'
    ).click() # Clica no participante

    sleep(0.5)

    # Verifica se o participante é administrador
    if element_exists(self,
        '//*[@id="app"]/div[1]/span[2]/div[1]/div/div/div/div/div/div/div[2]/div[1]/div/div/div/div/div/div[2]/div[1]/div[2]'
    ):
        
        # Caso sim, gera uma mensagem de erro
        print(f'{participant_name} is already an admin')
    
    else:
        # Caso não, clica no botão de promover para admin
        self.driver.find_element_by_xpath(
            '//*[@id="app"]/div[1]/span[4]/div/ul/div/li[1]/div[1]'
        ).click()

    self.driver.find_element_by_xpath(
        '//*[@id="app"]/div[1]/span[2]/div[1]/div/div/div/div/div/div/header/div/div[1]/button'
    ).click()

    logging.info(f"You made {participant_name} a admin group")
    close_info()


def select_chat_by_name(self, chat_name: str):
    """Go to the selected chat by its number

    Args:
        chat_name (str): Contact/Group name
    """

    self.driver.find_element_by_xpath(
       '//*[@id="side"]/div[1]/div/label/div/div[2]'
    ).send_keys(chat_name)

    self.driver.find_element_by_xpath(
        '//*[@id="side"]/div[1]/div/label/div/div[2]'
    ).send_keys(Keys.ENTER)
    logging.info(f"You selected the {chat_name} chat")


def select_chat_by_number(self, chat_number: int):
    """Go to the selected chat by its number

    Args:
        chat_number (int): Contact number. Example: 1NPAXXXXXXX
    """

    self.driver.get(f"https://web.whatsapp.com/send?phone={chat_number}")
    sleep(5)

    logging.info(f"You selected the {chat_number} chat")


def create_group(self, group_name: str, contacts: list):

    """Create a new whatsapp group

    Args:
        group_name (str): Name of the group
        contacts (list): List of contacts to add into the group
    """

    self.driver.find_element_by_xpath(
        '//*[@id="side"]/header/div[2]/div/span/div[3]/div/span'
    ).click()

    self.driver.find_element_by_xpath(
        '//*[@id="side"]/header/div[2]/div/span/div[3]/span/div[1]/ul/li[1]/div[1]'
    ).click()

    box = self.driver.find_element_by_xpath(
        '//*[@id="app"]/div[1]/div[1]/div[2]/div[1]/span/div[1]/span/div[1]/div/div[1]/div/div/input'
    )

    for contact in contacts:
        box.clear()
        box.send_keys(contact)
        box.send_keys(Keys.ENTER)

    self.driver.find_element_by_xpath(
        '//*[@id="app"]/div[1]/div[1]/div[2]/div[1]/span/div[1]/span/div[1]/div/span/div'
    ).click()

    self.driver.find_element_by_xpath(
        '//*[@id="app"]/div[1]/div[1]/div[2]/div[1]/span/div[1]/span/div[1]/div/div[2]/div/div[2]/div/div[2]'
    ).send_keys(group_name)

    self.driver.find_element_by_xpath(
        '//*[@id="app"]/div[1]/div[1]/div[2]/div[1]/span/div[1]/span/div[1]/div/span/div/div'
    ).click()
    
    sleep(2)

    if element_exists(self, 
        '//*[@id="app"]/div[1]/span[2]/div[1]/span/div[1]/div/div/div/div/div[2]/div[2]'
    ):

        self.driver.find_element_by_xpath(
            '//*[@id="app"]/div[1]/span[2]/div[1]/span/div[1]/div/div/div/div/div[2]/div[2]'
        ).click()
        
        self.driver.find_element_by_xpath(
            '//*[@id="app"]/div[1]/span[2]/div[1]/span/div[1]/div/div/div/div/div/div/span/div'
        ).click()

    logging.info(f"You created the group \"{group_name}\" with {contacts}")