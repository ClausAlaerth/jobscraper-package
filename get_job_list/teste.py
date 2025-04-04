from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time


class JobScraping:

    def __init__(self, domain: str):
        self.domain = domain
        self.lista: list[dict] = []
        self.navigator = webdriver.Chrome()
        self.wait = WebDriverWait(self.navigator, 10)

    def acessar(self):
        self.navigator.get(self.domain)

        # self.navigator.maximize_window()

        fic_list = self.wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "article > h2 > a")))

        for i in range(len(fic_list)):
            self.navigator.execute_script(
                "arguments[0].scrollIntoView({block: 'center'})", fic_list[i])

            name = fic_list[i].get_attribute("text")
            link = fic_list[i].get_attribute("href")

            self.lista.append({"Nome": name, "Link": link})

        print(len(fic_list))

        for i in self.lista:
            print(i["Nome"], i["Link"])

        time.sleep(100)


if __name__ == "__main__":

    scrape = JobScraping(domain="https://www.spiritfanfiction.com/recentes")

    scrape.acessar()
