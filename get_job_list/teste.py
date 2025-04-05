from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from conversion import list_conversion  # type: ignore
# import time

# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.service import Service
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


class JobScraping:

    def __init__(self, domain: str):
        self.domain = domain
        self.lista: list = []
        self.navigator = webdriver.Chrome()
        self.wait = WebDriverWait(self.navigator, 10)

    def acessar(self):
        self.navigator.get(self.domain)

        fic_list = self.wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "article > h2 > a")))

        for i in range(len(fic_list)):
            self.navigator.execute_script(
                "arguments[0].scrollIntoView({block: 'center'})", fic_list[i])

            name = fic_list[i].get_attribute("text")
            link = fic_list[i].get_attribute("href")

            self.lista.append([name, link])

        list_conversion(self.lista, "arquivotestedois", "fanfic")


if __name__ == "__main__":

    scrape = JobScraping(domain="https://www.spiritfanfiction.com/recentes")

    scrape.acessar()
