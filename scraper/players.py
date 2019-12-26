from scraper.biwenger_scraper import BiwengerScraper

from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
import pandas as pd
import logging
import time
import os


class PlayerScraper(BiwengerScraper):
    def __init__(self, config, args):
        super(PlayerScraper, self).__init__(config, args["headless"])
        self.downloads_folder = args["downloads_folder"]
        self.league_index = args["league_index"]
        self.input_file = args["input_file"]
        self.start_page = args["start_page"]
        self.headless = args["headless"]

    def scrape(self):

        transfers_df = pd.read_csv("data/{0}".format(self.input_file))
        selected_players = transfers_df.player_name.unique()

        self.login()

        # Go to players view
        self.click(self.driver.find_element_by_link_text('Players'))

        # Iterate pagination
        current_page = 1

        while True:
            try:
                if self.start_page > current_page:
                    logging.info("Skipping page {0}".format(current_page))
                else:
                    # Collect information of the players shown in the current page
                    for player in self.driver.find_elements_by_tag_name("player-card"):

                        player_name = player.find_element_by_xpath(".//h3[@itemprop='name']/a").text
                        if player_name not in selected_players:
                            continue

                        player_info = {
                            "name": player_name,
                            "team": player.find_element_by_xpath(".//a[@class='team']").get_attribute("title"),
                            "position": player.find_element_by_xpath(".//player-position").get_attribute("title")
                        }

                        # Go to player's view
                        self.click(player.find_element_by_xpath(".//h3[@itemprop='name']/a"))

                        # Get player's market value, position and team
                        player_info["value"] = self.driver.find_element_by_xpath("//span[@itemprop='netWorth']").text


                        point_list = self.driver.find_element_by_tag_name("point-list")

                        rounds = []
                        points = []
                        for round in point_list.find_elements_by_xpath(".//table/tr"):
                            rows = round.find_elements_by_xpath(".//td")
                            if len(rows) > 1:
                                rounds.append(rows[0].text[:3])
                                points.append(rows[-2].text)

                        player_info["rounds"] = rounds
                        player_info["points"] = points

                        # Download value time series in CSV
                        tab = self.driver.find_element_by_xpath("//tabs/ul/li[2]/a")
                        self.driver.execute_script("arguments[0].click();", tab)
                        element = self.driver.find_element_by_xpath("//chartjs/div/btn-group/button/i[contains(@class, 'icon-download')]")
                        self.driver.execute_script("arguments[0].click();", element)

                        time.sleep(10)

                        os.rename("{0}/chart.csv".format(self.downloads_folder),
                                  "data/player_values/{0}.csv".format(player_name))

                        logging.debug(player_info)

                        # Close player's view
                        self.click(self.driver.find_element_by_xpath("//i[@title='Close']"))

                    logging.info("Page {0} scraped".format(current_page))

            except (NoSuchElementException, ElementNotInteractableException):
                logging.info("Blacklisted because of max. requets")
                logging.info("Current page: {0}".format(current_page))
                break

            # Click on next page button if available, otherwise end loop
            next_page_button = self.driver.find_elements_by_xpath("//ul[@class='pagination']/li")[-2]
            if next_page_button.is_enabled():
                self.click(next_page_button)
                current_page += 1
            else:
                logging.info("Market scraper finished")
                break
