from scraper.biwenger_scraper import BiwengerScraper

from selenium.common.exceptions import NoSuchElementException
import logging
import time


class TeamScraper(BiwengerScraper):
    def __init__(self, config, args):
        super(TeamScraper, self).__init__(config, args["headless"])
        self.league_index = args["league_index"]
        self.headless = args["headless"]

    def scrape(self):
        self.login()
        self.choose_league(self.league_index)

        # Go to teams view
        self.driver.find_element_by_link_text('League').click()
        time.sleep(1)


        # TODO