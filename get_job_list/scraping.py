from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time


class JobScraping:

    def __init__(
            self, user: str,
            password: str,
            domain: str,
            query: list[str]
    ):
        self.user = user
        self.password = password
        self.domain = domain
        self.query = query
        # self.location = location
        # self.job_list_archive = []
        self.navigator = webdriver.Chrome()
        self.wait = WebDriverWait(self.navigator, 10)

    def __domain_selector(self):
        if self.domain == "linkedin":
            self.domain = "https://www.linkedin.com/jobs/"
            self.__acessar_linkedin()
            return
        else:
            ...

    def __acessar_linkedin(self):

        # go to domain
        self.navigator.get(self.domain)

        # self.navigator.maximize_window()

        # login stage
        user_input = self.wait.until(
            EC.presence_of_element_located((By.XPATH, "/html/body/main/section[1]/div/div/form/div[1]/div[1]/div/div/input")))  # noqa: E501
        user_input.send_keys(self.user)

        password_input = self.wait.until(
            EC.presence_of_element_located((By.XPATH, "/html/body/main/section[1]/div/div/form/div[1]/div[2]/div/div/input")))  # noqa: E501
        password_input.send_keys(self.password)

        # time for auth
        time.sleep(15)

        # using queries
        for i in self.query:

            query_input_xpath = "/html/body/div[6]/header/div/div/div/div[2]/div[2]/div/div/input[1]"  # noqa: E501
            query_input = self.wait.until(
                EC.presence_of_element_located((By.XPATH, query_input_xpath)))
            query_input.send_keys(i)

            query_input.send_keys(Keys.ENTER)

            time.sleep(5)

            # scrape the jobs
            job_list = self.navigator.find_elements(
                By.CSS_SELECTOR, "div > div > a")

            print(job_list)

            for j in range(len(job_list)):

                # script to scroll
                self.navigator.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'})", job_list[j])  # noqa: E501

                individual_job_label = job_list[j].get_attribute("aria-label")
                individual_job_link = job_list[j].get_attribute("href")

                # remove after testing
                print(individual_job_label, individual_job_link)

                # self.job_list_archive.append({"Job Name": individual_job_label, "Job Link": individual_job_link})  # noqa: E501

            self.navigator.back()

        time.sleep(100)  # remove after testing

    def criar_arquivo(self):
        self.__domain_selector()
        # função do arquivo entra aqui (dict, path)


if __name__ == "__main__":

    query = [
        '("python" AND "junior")',
        '("analista de dados" AND "junior")',
        '("analista de suporte" AND "junior")'
    ]

    scrape = JobScraping(
        user="lc.aquinodeoliveira@gmail.com",
        password="4udacious_4_Aquin0",
        domain="linkedin",
        query=query
    )

    scrape.criar_arquivo()
