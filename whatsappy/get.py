from time import sleep

from .tool import close_info, is_admin


def get_recent_chats(self):
    """Returns a list of all recent chats

    Returns:
        List: All the recent chats
    """

    array = self.driver.execute_script("""
        function getElementByXpath(path) {
            return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
        } // Cria uma função que retorna os elementos pelo XPATH

        // Armazena a classe do elemento das conversas
        let elemClass = getElementByXpath('//*[@id="pane-side"]/div[1]/div/div/div[1]').className

        // Procura pelos elementos
        let contacts = document.querySelectorAll(`.${elemClass}`);
        let newArray = new Array();

        // Armazena a classe do nome dos contatos
        let nameClass = getElementByXpath('//*[@id="pane-side"]/div[1]/div/div/div[1]/div/div/div[2]/div[1]/div[1]/span/span')className.split(' ')[0]

        // Separa o nome dos elementos e coloca em um Array
        for (var i = 0; i < contacts.length; i++){
            newArray.push(contacts[i].querySelector(`.${nameClass}`).title);
        };

        // Retorna o Array com os contatos recentes
        return newArray;
    """)

    return array


def get_pinned_chats(self):
    """Returns a list of all pinned chats

    Returns:
        List: All the pinned chats
    """

    array = self.driver.execute_script("""
        function getElementByXpath(path) {
            return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
        } // Cria uma função que retorna os elementos pelo XPATH

        // Armazena a classe do elemento das conversas fixadas
        let elemClass = getElementByXpath('//*[@id="pane-side"]/div[1]/div/div/div[1]/div/div/div[2]/div[2]/div[2]/span[1]/div')className.split(' ')[1]
        
        // Busca pelos elementos
        let pin = document.querySelectorAll(`.${elemClass}`);

        // Armazena a classe do nome dos contatos
        let nameClass = getElementByXpath('//*[@id="pane-side"]/div[1]/div/div/div[1]/div/div/div[2]/div[1]/div[1]/span/span')className.split(' ')[0]
        let newArray = new Array();

        // Separa o nome dos elementos em um Array
        for (var i = 0; i < pin.length; i++) {
            newArray.push(pin[i].parentNode.parentNode.parentNode.parentNode.querySelector(`.${nameClass}`).title)
        }

        // Retorna o array com os contatos fixados
        return newArray
    """)

    return array


def get_group_invite_link(self):
    """Returns group invite link

    Returns:
        str: Group invite link
    """

    # Abre as informações do grupo
    self.driver.find_element_by_xpath('//*[@id="main"]/header/div[2]').click()

    if not is_admin(self):
        print("You are not a group admin!")
        return

    self.driver.find_element_by_xpath(
        '//*[@id="app"]/div[1]/div[1]/div[2]/div[3]/span/div[1]/span/div[1]/div/section/div[5]/div[3]'
    ).click() # Clica em convidar para grupo via link

    sleep(1)

    group_link = self.driver.find_element_by_xpath(
        '//*[@id="group-invite-link-anchor"]'
    ).text # Armazena o link de convite

    self.driver.find_element_by_xpath(
        '//*[@id="app"]/div[1]/div[1]/div[2]/div[3]/span/div[1]/span/div[1]/header/div/div[1]/button'
    ).click() # Sai das informações do link

    sleep(0.5)

    close_info(self)

    return group_link # Retorna o link de convite
