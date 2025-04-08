from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from conversion import list_conversion  # type: ignore

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from selenium.common.exceptions import TimeoutException

import time


class JobScraper:

    def __init__(
            self,
            domain: str,
            archive_name: str,
            query: list,
            location: str
    ):
        self.domain = domain
        self.archive_name = archive_name
        self.sheet_name = domain
        self.query = query
        self.location = location
        self.job_archive: list = []
        self.processed_archive: list = []

        self.options = Options()
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--ignore-ssl-errors')
        self.options.add_argument('--log-level=3')

        self.navigator = webdriver.Chrome(
            options=self.options, service=Service(ChromeDriverManager().install()))  # noqa: E501
        self.wait = WebDriverWait(self.navigator, 18)

    def __domain_selector(self):
        if self.domain == "linkedin":
            self.domain = "https://www.linkedin.com/jobs/"
            self.__acessar_linkedin()
            return
        elif self.domain == "vagas.com":
            self.domain = "https://www.vagas.com.br/"
            self.__acessar_vagas()
            return
        elif self.domain == "catho":
            self.domain = "https://www.catho.com.br"
            self.__acessar_catho()
            return
        elif self.domain == "glassdoor":
            self.domain = "https://www.glassdoor.com.br/Vaga/index.htm"
            self.__acessar_glassdoor()
            return
        else:
            raise NotImplementedError(
                "Você não usou uma palavra-chave apropriada."
            )

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

            # time to load assets
            time.sleep(3)

            time.sleep(2)

            # scrape the jobs
            try:
                job_list = self.navigator.find_elements(
                    By.CSS_SELECTOR, "li div > div > a")
            except TimeoutException:
                job_list = False

            if job_list:

                for j in range(len(job_list)):

                    # script to scroll
                    self.navigator.execute_script(
                        "arguments[0].scrollIntoView({block: 'center'})", job_list[j])  # noqa: E501

                    individual_job_label = job_list[j].get_attribute(
                        "aria-label")
                    individual_job_link = job_list[j].get_attribute("href")

                    self.job_archive.append(
                        [individual_job_label, individual_job_link])

                self.navigator.back()

            else:
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
            query_input.send_keys(i + " " + self.location)
            query_input.send_keys(Keys.ENTER)

            # time to load assets
            time.sleep(3)

            # scraping job
            try:
                job_list = self.wait.until(EC.presence_of_all_elements_located(
                    (By.CLASS_NAME, "link-detalhes-vaga")))
            except TimeoutException:
                job_list = False

            if job_list:

                for j in range(len(job_list)):

                    # script to scroll
                    self.navigator.execute_script(
                        "arguments[0].scrollIntoView({block: 'center'})", job_list[j])  # noqa: E501

                    individual_job_label = job_list[j].get_attribute("title")
                    individual_job_link = job_list[j].get_attribute("href")

                    self.job_archive.append(
                        [individual_job_label, individual_job_link])

                self.navigator.get(self.domain)

            else:
                self.navigator.get(self.domain)

        self.__dupe_removal(self.job_archive)

    def __acessar_catho(self):

        # go to domain
        self.navigator.get(self.domain)

        # using queries
        for i in self.query:

            query_input = self.wait.until(EC.presence_of_element_located(
                (By.ID, "input-0")))
            query_input.send_keys(i)
            query_input.send_keys(Keys.ENTER)

            # treating location for url
            treated_location = "-".join(self.location.split()).lower()
            self.navigator.get(self.navigator.current_url + treated_location)

            # time to load assets
            time.sleep(3)

            # scraping job
            try:
                job_list = self.wait.until(EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "#search-result > ul > li div > h2 > a")))  # noqa: E501
            except TimeoutException:
                job_list = False

            if job_list:

                for j in range(len(job_list)):

                    # script to scroll
                    self.navigator.execute_script(
                        "arguments[0].scrollIntoView({block: 'center'})", job_list[j])  # noqa: E501

                    individual_job_title = job_list[j].get_attribute("text")
                    individual_job_link = job_list[j].get_attribute("href")

                    self.job_archive.append(
                        [individual_job_title, individual_job_link])

                self.navigator.get(self.domain)

            else:
                self.navigator.get(self.domain)

        self.__dupe_removal(self.job_archive)

    def __acessar_glassdoor(self):

        # go to domain
        self.navigator.get(self.domain)

        # using queries
        for i in self.query:

            query_input = self.wait.until(EC.presence_of_element_located(
                (By.ID, "searchBar-jobTitle")))
            query_input.send_keys(i)

            location_input = self.wait.until(EC.presence_of_element_located(
                (By.ID, "searchBar-location")))
            location_input.send_keys(self.location)
            location_input.send_keys(Keys.ENTER)

            # time to load assets
            time.sleep(3)

            # scraping job
            try:
                job_list = self.wait.until(EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "a.JobCard_jobTitle__GLyJ1")))  # noqa: E501
            except TimeoutException:
                job_list = False

            if job_list:

                for j in range(len(job_list)):

                    # time.sleep(0.5)

                    # script to scroll
                    self.navigator.execute_script(
                        "arguments[0].scrollIntoView({block: 'center'})", job_list[j])  # noqa: E501

                    individual_job_title = job_list[j].get_attribute("text")
                    individual_job_link = job_list[j].get_attribute("href")

                    self.job_archive.append(
                        [individual_job_title, individual_job_link])

                self.navigator.back()

            else:
                self.navigator.back()

        self.__dupe_removal(self.job_archive)

    def criar_arquivo(self):
        self.__domain_selector()
        list_conversion(
            self.processed_archive,
            self.archive_name,
            self.sheet_name
        )


if __name__ == "__main__":

    query = [
        "python junior",
        "python backend junior",
        "python junior",
        "analista de dados junior",
        "analista de sistemas junior",
        "django junior",
    ]

    # linkedin = JobScraper(
    #     "linkedin",
    #     "lista_de_vagas",
    #     query,
    #     "Rio de Janeiro"
    # )

    # vagas = JobScraper(
    #     "vagas.com",
    #     "lista_de_vagas",
    #     query,
    #     "Rio de Janeiro"
    # )

    catho = JobScraper(
        "catho",
        "lista_de_vagas",
        query,
        "RJ"
    )

    # glassdoor = JobScraper(
    #     "glassdoor",
    #     "lista_de_vagas",
    #     query,
    #     "Rio de Janeiro"
    # )

    catho.criar_arquivo()
