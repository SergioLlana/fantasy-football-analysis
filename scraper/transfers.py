from scraper.biwenger_scraper import BiwengerScraper

import logging


class TransferScraper(BiwengerScraper):
    def __init__(self, config, args):
        super(TransferScraper, self).__init__(config, args["headless"])
        self.league_index = args["league_index"]
        self.headless = args["headless"]

    def scrape(self):
        self.login()
        self.choose_league(self.league_index)

        self.scroll_down()

        for transfers in self.driver.find_elements_by_tag_name("transfer-list"):

            date = transfers.find_element_by_xpath(".//../div[contains(@class, 'timeline-actions')]/div/time-relative").get_attribute("title")

            for player in transfers.find_elements_by_tag_name("player-card"):
                transfer_info = player.find_element_by_xpath(
                    ".//div[contains(@class, 'content')]/div[contains(@class, 'main')]/dynamic-expression-container")

                player_name = player.find_element_by_xpath(".//h3/a").text
                money = transfer_info.find_element_by_xpath(".//strong").text

                transfer_text = transfer_info.text
                if transfer_text.startswith("Changes to"):
                    origin_user = None
                    destination_user = transfer_info.find_element_by_xpath(".//user-link/a").text
                elif transfer_text.startswith("Sold by"):
                    origin_user = transfer_info.find_element_by_xpath(".//user-link/a").text
                    destination_user = None
                elif transfer_text.startswith("Changes for"):
                    origin_user = transfer_info.find_element_by_xpath(".//user-link[1]/a").text
                    destination_user = transfer_info.find_element_by_xpath(".//user-link[2]/a").text

                logging.debug({
                    "player_name": player_name, "money": money, "date": date,
                    "origin_user": origin_user, "destination_user": destination_user
                })

        logging.info("Transfers scraper finished")

