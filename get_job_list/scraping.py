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
            query: list[str],
            location: str):
        self.user = user
        self.password = password
        self.domain = domain
        self.query = query
        self.location = location
        # self.job_list_archive = []
        self.navigator = webdriver.Chrome()
        self.wait = WebDriverWait(self.navigator, 10)

    def acessar(self):
        self.navigator.get(self.domain)

        self.navigator.maximize_window()

        # login stage
        user_input = self.wait.until(
            EC.presence_of_element_located((By.XPATH, "/html/body/main/section[1]/div/div/form/div[1]/div[1]/div/div/input")))
        user_input.send_keys(self.user)

        password_input = self.wait.until(
            EC.presence_of_element_located((By.XPATH, "/html/body/main/section[1]/div/div/form/div[1]/div[2]/div/div/input")))
        password_input.send_keys(self.password)

        # user_input = self.wait.until(
        #     EC.presence_of_element_located((By.ID, "username")))
        # user_input.send_keys(self.user)

        # password_input = self.wait.until(
        #     EC.presence_of_element_located((By.ID, "password")))
        # password_input.send_keys(self.password)

        # password_input.send_keys(Keys.ENTER)

        # time for auth
        time.sleep(15)

        # go to jobs
        # job_domain_xpath = '//*[@id="global-nav"]/div/nav/ul/li[3]/a'
        # job_domain_button = self.wait.until(
        #     EC.presence_of_element_located((By.XPATH, job_domain_xpath)))

        # job_domain_button.click()

        # query insertion
        for i in self.query:

            query_input_xpath = "/html/body/div[6]/header/div/div/div/div[2]/div[2]/div/div/input[1]"
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
                    "arguments[0].scrollIntoView({block: 'center'})", job_list[j])

                individual_job_label = job_list[j].get_attribute("aria-label")
                individual_job_link = job_list[j].get_attribute("href")

                print(individual_job_label, individual_job_link)

                # self.job_list_archive.append({"Job Name": individual_job_label, "Job Link": individual_job_link})

            self.navigator.back()

        time.sleep(100)


if __name__ == "__main__":

    query = [
        '("python" AND "junior")',
        '("analista de dados" AND "junior")',
        '("analista de suporte" AND "junior")'
    ]

    scrape = JobScraping(
        user="lc.aquinodeoliveira@gmail.com",
        password="4udacious_4_Aquin0",
        domain="https://www.linkedin.com/login",
        query=query,
        location="Rio de Janeiro, Brasil")

    scrape.acessar()
