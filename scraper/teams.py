from scraper.biwenger_scraper import BiwengerScraper

import logging


class TeamScraper(BiwengerScraper):
    def __init__(self, config, args):
        super(TeamScraper, self).__init__(config, args["headless"])
        self.league_index = args["league_index"]
        self.headless = args["headless"]

    def scrape(self):
        self.login()
        self.choose_league(self.league_index)

        # Go to teams view
        self.click(self.driver.find_element_by_xpath("//a[@href='/league']"))

        # Collect information of the players shown in the current page
        for user in self.driver.find_elements_by_tag_name("user-card"):
            user_info = {"name": user.find_element_by_xpath(".//h3/a").text}

            # Go to user's view
            self.click(user.find_element_by_xpath(".//h3/a"))

            # Get user's market value, position and team
            stats = self.driver.find_elements_by_xpath("//div[@class='body']/div[@class='stats']//span")
            user_info["points"] = stats[4].text
            user_info["value"] = stats[5].text

            # Get user's players
            players = self.driver.find_elements_by_tag_name("player-card")

            player_names = []
            purcharses_info = []
            for player in players:
                purcharses_info.append(player.find_element_by_xpath(".//player-owner/span").text)
                player_names.append(player.find_element_by_xpath(".//h3[@itemprop='name']/a").text)

            user_info["purchase_info"] = purcharses_info
            user_info["players"] = player_names

            logging.debug(user_info)

            # Close user's view
            self.click(self.driver.find_element_by_xpath("//i[@title='Close']"))

        logging.info("Team scraper finished")

