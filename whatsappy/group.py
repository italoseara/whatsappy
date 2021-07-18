from time import sleep
from selenium.webdriver.common.keys import Keys
from os import path
from .tool import *
from .error import BadPathError
import traceback


def change_group_description(self, description: str):
    """Changes the group description

    Args:
        description (str): New group description
    """

    try:

        # Abre as informações do grupo
        self.driver.find_element_by_xpath('//*[@id="main"]/header/div[2]').click()

        if not is_admin(self):
            print("You are not a group admin!")
            return

        self.driver.find_element_by_xpath(
            '//*[@id="app"]/div[1]/div[1]/div[2]/div[3]/span/div[1]/span/div[1]/div/section/div[2]/div[2]/div/div/span[2]/div'
        ).click() # Tenta clicar na caneta de edição da descrição

        description_dom = self.driver.find_element_by_xpath(
            '//*[@id="app"]/div[1]/div[1]/div[2]/div[3]/span/div[1]/span/div[1]/div/section/div[2]/div[2]/div/div[1]/div/div[2]'
        ) # Seleciona a descrição para editar

        description_dom.clear() # Limpa

        if description.find("\n"): # Escreve
            for line in description.split("\n"):
                description_dom.send_keys(line)
                description_dom.send_keys(Keys.SHIFT + Keys.ENTER)
            description_dom.send_keys(Keys.ENTER)

        else:
            description_dom.send_keys(description)

    except:
        error_log(traceback.format_exc())

    try: # Fecha as informações do grupo
        self.driver.find_element_by_xpath(
            '//*[@id="app"]/div[1]/div[1]/div[2]/div[3]/span/div[1]/span/div[1]/header/div/div[1]/button'
        ).click()
    except:
        pass


def change_group_name(self, name: str):
    """Changes the group name

    Args:
        name (str): New group name
    """

    try:

        # Abre as informações do grupo
        self.driver.find_element_by_xpath('//*[@id="main"]/header/div[2]').click()

        if not is_admin(self):
            print("You are not a group admin!")
            return

        # Clica para editar o nome do grupo
        self.driver.find_element_by_xpath(
            '//*[@id="app"]/div[1]/div[1]/div[2]/div[3]/span/div[1]/span/div[1]/div/section/div[1]/div[2]/div[1]/span[2]/div'
        ).click()

        group_name_dom = self.driver.find_element_by_xpath(
            '//*[@id="app"]/div[1]/div[1]/div[2]/div[3]/span/div[1]/span/div[1]/div/section/div[1]/div[2]/div[1]/div/div[2]'
        ) # Seleciona o texto do nome do grupo

        group_name_dom.clear() # Limpa
        group_name_dom.send_keys(name + Keys.ENTER) # Escreve

    except:
        error_log(traceback.format_exc())

    try:
        self.driver.find_element_by_xpath(
            '//*[@id="app"]/div[1]/div[1]/div[2]/div[3]/span/div[1]/span/div[1]/header/div/div[1]/button'
        ).click() # Fecha as informações do grupo
    except:
        pass


def change_group_pfp(self, file_path: str):

    try:

        if not path.isabs(file_path):
            raise BadPathError("The file path is not absolute")

        # Abre as informações do grupo
        self.driver.find_element_by_xpath('//*[@id="main"]/header/div[2]').click()

        if not is_admin(self):
            print("You are not a group admin!")
            return

        self.driver.find_element_by_xpath(
            '//*[@id="app"]/div[1]/div[1]/div[2]/div[3]/span/div[1]/span/div[1]/div/section/div[1]/div[1]/div/input'
        ).send_keys(file_path) # Envia a foto

        sleep(1)

        self.driver.find_element_by_xpath(
            '//*[@id="app"]/div[1]/span[2]/div[1]/div/div/div/div/div/span/div[1]/div/div[2]/span/div'
        ).click() # Confima

    except:
        error_log(traceback.format_exc())

    try:
        self.driver.find_element_by_xpath(
            '//*[@id="app"]/div[1]/div[1]/div[2]/div[3]/span/div[1]/span/div[1]/header/div/div[1]/button'
        ).click() # Fecha as informações do grupo
    except:
        pass


def leave_group(self):
    """Leaves the group you are"""

    # Abre as informações do grupo
    self.driver.find_element_by_xpath('//*[@id="main"]/header/div[2]').click()

    self.driver.find_element_by_xpath(
        '//*[@id="app"]/div[1]/div[1]/div[2]/div[3]/span/div[1]/span/div[1]/div/section/div[6]/div'
    ).click()

    self.driver.find_element_by_xpath(
        '//*[@id="app"]/div[1]/span[2]/div[1]/div/div/div/div/div/div[2]/div[2]'
    ).click()
