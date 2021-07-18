def error_log(error):
    print(error)

    with open("error.log", "a+") as f:
        f.writelines(f"[ERROR] {error}")
        f.writelines("=" * 100 + "\n")


def element_exists(self, xpath: str):
    return self.driver.execute_script(
        f'return !!document.evaluate(\'{xpath}\', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;'
    )


def is_admin(self):
    return element_exists(self,
        '//*[@id="app"]/div[1]/div[1]/div[2]/div[3]/span/div[1]/span/div[1]/div/section/div[5]/div[2]/div[2]'
    )
    