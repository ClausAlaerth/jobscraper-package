from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from conversion import list_conversion  # type: ignore

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

import time


class JobScraper:

    def __init__(
            self,
            domain: str,
            archive_name: str,
            query: list
    ):
        self.domain = domain
        self.archive_name = archive_name
        self.sheet_name = domain
        self.query = query
        self.job_archive: list = []
        self.processed_archive: list = []

        self.options = Options()
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--ignore-ssl-errors')
        self.options.add_argument('--log-level=3')

        self.navigator = webdriver.Chrome(
            options=self.options, service=Service(ChromeDriverManager().install()))  # noqa: E501
        self.wait = WebDriverWait(self.navigator, 30)

    def __domain_selector(self):
        if self.domain == "linkedin":
            self.domain = "https://www.linkedin.com/jobs/"
            self.__acessar_linkedin()
            return
        if self.domain == "vagas.com":
            self.domain = "https://www.vagas.com.br/"
            self.__acessar_vagas()
            return
        else:
            ...

    def __dupe_removal(self, archive):
        self.processed_archive = list(
            set(list(tuple(x) for x in archive)))

    def __acessar_linkedin(self):

        # go to domain
        self.navigator.get(self.domain)
        # self.navigator.maximize_window()

        # using queries
        for i in self.query:

            query_input = self.wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div > div > div.relative > input")))
            query_input.send_keys(i)

            query_input.send_keys(Keys.ENTER)

            time.sleep(2)

            # scrape the jobs
            job_list = self.navigator.find_elements(
                By.CSS_SELECTOR, "li div > div > a")

            for j in range(len(job_list)):

                # script to scroll
                self.navigator.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'})", job_list[j])  # noqa: E501

                individual_job_label = job_list[j].get_attribute("aria-label")
                individual_job_link = job_list[j].get_attribute("href")

                self.job_archive.append(
                    [individual_job_label, individual_job_link])

            self.navigator.back()

        self.__dupe_removal(self.job_archive)

    def __acessar_vagas(self):

        # go to domain
        self.navigator.get(self.domain)
        # self.navigator.maximize_window()

        # using queries
        for i in self.query:

            query_input = self.wait.until(EC.presence_of_element_located(
                (By.ID, "nova-home-search")))
            query_input.send_keys(i)

            query_input.send_keys(Keys.ENTER)

            # scraping job
            job_list = self.wait.until(EC.presence_of_all_elements_located(
                (By.CLASS_NAME, "link-detalhes-vaga")))

            for j in range(len(job_list)):

                # script to scroll
                self.navigator.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'})", job_list[j])  # noqa: E501

                individual_job_label = job_list[j].get_attribute("title")
                individual_job_link = job_list[j].get_attribute("href")

                self.job_archive.append(
                    [individual_job_label, individual_job_link])

            self.navigator.back()
            self.navigator.refresh()

        self.__dupe_removal(self.job_archive)

    def criar_arquivo(self):
        self.__domain_selector()
        list_conversion(
            self.processed_archive,
            self.archive_name,
            self.sheet_name
        )


if __name__ == "__main__":

    #     query = [
    #         "('python' AND 'junior')",
    #         "('analista' AND 'junior')",
    #         "('dados' AND 'junior')",
    #     ]

    #     linkedin = JobScraper(
    #         "linkedin",
    #         "lista_de_vagas",
    #         query=query
    #     )

    # linkedin.criar_arquivo()

    query = [
        "python junior rio de janeiro",
        "analista junior rio de janeiro",
        "dados junior rio de janeiro",
    ]

    vagas = JobScraper(
        "vagas.com",
        "lista_de_vagas",
        query=query
    )

    vagas.criar_arquivo()
