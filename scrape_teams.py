from utils import parse_team_scraper_args, read_json
from scraper.teams import TeamScraper
import logging


def scrape(args):
    config = read_json("scraper/config/config.json")
    scraper = TeamScraper(config, args)
    scraper.scrape()


if __name__ == "__main__":
    logging.basicConfig(level="DEBUG", format="%(message)s", filename="data/ranking.log")
    logging.getLogger('selenium').setLevel(logging.CRITICAL)
    logging.getLogger("urllib3").setLevel(logging.CRITICAL)

    console = logging.StreamHandler()
    console.setLevel("INFO")
    console.setFormatter(logging.Formatter("%(message)s"))
    logging.getLogger("").addHandler(console)

    logging.info("STARTING BIWENGER SCRAPER")

    args = parse_team_scraper_args()
    scrape(args)

    logging.info("PROCESS FINISHED")

