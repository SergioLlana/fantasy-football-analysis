from utils import parse_scraper_args, read_json
from scraper.transfers import TransferScraper
from scraper.players import PlayerScraper
from scraper.market import MarketScraper
from scraper.teams import TeamScraper
import logging


def scrape(scraper, args):
    config = read_json("scraper/config/config.json")
    scraper_instance = scraper(config, args)
    scraper_instance.scrape()


if __name__ == "__main__":
    args = parse_scraper_args()
    if args["scraper_type"] == "market":
        scraper = MarketScraper
        output_file = "market.log"
    elif args["scraper_type"] == "transfers":
        scraper = TransferScraper
        output_file = "transfers.log"
    elif args["scraper_type"] == "players":
        scraper = PlayerScraper
        output_file = "players.log"
    else:
        scraper = TeamScraper
        output_file = "users.log"

    logging.basicConfig(level="DEBUG", format="%(message)s",
                        filename="data/{0}".format(output_file))

    logging.getLogger('selenium').setLevel(logging.CRITICAL)
    logging.getLogger("urllib3").setLevel(logging.CRITICAL)

    console = logging.StreamHandler()
    console.setLevel("INFO")
    console.setFormatter(logging.Formatter("%(message)s"))
    logging.getLogger("").addHandler(console)

    logging.info("STARTING BIWENGER SCRAPER")

    scrape(scraper, args)

    logging.info("PROCESS FINISHED")
