from scraper.biwenger_scraper import BiwengerScraper

from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.support.ui import Select
import logging
import time


class MarketScraper(BiwengerScraper):
    def __init__(self, config, args):
        super(MarketScraper, self).__init__(config, args["headless"])
        self.league_index = args["league_index"]
        self.start_page = args["start_page"]
        self.headless = args["headless"]

    def scrape(self):
        self.login()
        self.choose_league(self.league_index)

        # Go to players view
        self.click(self.driver.find_element_by_link_text('Players'))

        # Iterate pagination
        current_page = 1
        while True:

            # Skip page until we arrive to start_page
            if self.start_page > current_page:
                logging.info("Skipping page {0}".format(current_page))
                continue

            # Collect information of the players shown in the current page
            for player in self.driver.find_elements_by_tag_name("player-card"):

                player_info = {
                    "name": player.find_element_by_xpath(".//h3[@itemprop='name']/a").text,
                    "team": player.find_element_by_xpath(".//a[@class='team']").get_attribute("title"),
                    "position": player.find_element_by_xpath(".//player-position").get_attribute("title")
                }

                # Go to player's view
                self.click(player.find_element_by_xpath(".//h3[@itemprop='name']/a"))

                # Get player's market value, position and team
                player_info["value"] = self.driver.find_element_by_xpath("//span[@itemprop='netWorth']").text

                # Whether the player is free or not
                try:
                    player_owner = self.driver.find_element_by_tag_name("player-owner")
                    player_info["free"] = False
                except:
                    player_info["free"] = True

                # Go to last season's stats and get players stats
                try:
                    selects = self.driver.find_elements_by_xpath('//player-detail-points/p/select')
                    seasons = Select(selects[0])
                    seasons.select_by_visible_text('2018/2019 season')
                    time.sleep(2)

                    seasons = Select(selects[1])
                    seasons.select_by_visible_text('AS.com and SofaScore average')
                    time.sleep(2)

                    stat_divs = self.driver.find_elements_by_xpath("//div[@class='stat main']")
                    player_info["points"] = stat_divs[0].find_element_by_tag_name("span").text
                    player_info["games"] = stat_divs[2].find_element_by_tag_name("span").text
                    goals_and_cards_div = stat_divs[2].find_element_by_tag_name("div").find_elements_by_tag_name("div")
                    player_info["goals"] = goals_and_cards_div[0].find_element_by_tag_name("span").text
                    player_info["cards"] = goals_and_cards_div[1].find_element_by_tag_name("span").text

                    logging.debug(player_info)

                    #  Close player's view
                    self.click(self.driver.find_element_by_xpath("//i[@title='Close']"))

                except (NoSuchElementException, ElementNotInteractableException):
                    logging.info("Blacklisted because of max. requets")
                    logging.info("Current page: {0}".format(current_page))
                    break

            logging.info("Page {0} scraped".format(current_page))

            # Click on next page button if available, otherwise end loop
            next_page_button = self.driver.find_elements_by_xpath("//ul[@class='pagination']/li")[-2]
            if next_page_button.is_enabled():
                self.click(next_page_button)
            else:
                logging.info("Market scraper finished")
                break
