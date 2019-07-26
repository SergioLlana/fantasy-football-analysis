from abc import ABC, abstractmethod
from selenium import webdriver
import time


class BiwengerScraper(ABC):
    def __init__(self, config, headless):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")

        if headless:
            options.add_argument('headless')

        self.driver = webdriver.Chrome(executable_path=config["chrome_path"], chrome_options=options)
        self.config = config

    @staticmethod
    def click(element, index=0, wait=2):
        if isinstance(element, list):
            element[index].click()
        else:
            element.click()
        time.sleep(wait)

    def login(self):
        self.driver.get(self.config["login_endpoint"])

        # Click on "Ya tengo cuenta"
        self.click(self.driver.find_element_by_tag_name('button'))

        # Login on the website
        username = self.driver.find_element_by_name("email")
        password = self.driver.find_element_by_name("password")
        username.send_keys(self.config["email"])
        password.send_keys(self.config["password"])

        # Submit form
        self.click(self.driver.find_element_by_tag_name('button'), wait=5)

    def choose_league(self, league_index):
        self.click(self.driver.find_element_by_id("menuToggle"), wait=3)
        self.click(self.driver.find_elements_by_xpath("//a[@class='league']/img"), index=league_index-1)

    @abstractmethod
    def scrape(self):
        pass
