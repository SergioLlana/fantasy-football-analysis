import argparse
import json
import sys


def parse_scraper_args():
    parser = argparse.ArgumentParser()

    # Whether we want to scrape the players in the market or the users in the league
    parser.add_argument('-t', '--scraper_type', dest='scraper_type', help='Scraper type',
                        choices=["market", "users"], default="users")

    # Whether the scraper will run in background or not
    parser.add_argument('-b', '--headless', dest='headless', help='Headless',
                        action='store_true', default=False)

    # League selector from 1 to num_leagues
    parser.add_argument('-l', '--league_index', dest='league_index',
                        help='League index', default="1")

    # Page of the market where the scraper starts to collect information (only for scraper_type="market")
    parser.add_argument('-p', '--start_page', dest='start_page',
                        help='Start page', default="1")

    args = parser.parse_args(sys.argv[1:])
    return {"league_index": int(args.league_index), "start_page": int(args.start_page),
            "headless": args.headless, "scraper_type": args.scraper_type}


def parse_parser_args():
    parser = argparse.ArgumentParser()

    # Whether we want to scrape the players in the market or the users in the league
    parser.add_argument('-t', '--log_type', dest='log_type', help='Log type',
                        choices=["market", "users"], default="users")

    # Name of the CSV
    parser.add_argument('-o', '--output_file', dest='output_file', help='Output file')

    args = parser.parse_args(sys.argv[1:])
    return {"output_file": args.output_file, "log_type": args.log_type}


def parse_simulator_args():
    parser = argparse.ArgumentParser()

    # Number of simulations
    parser.add_argument('-s', '--num_simulations', dest='num_simulations',
                        help='Number of simulations', default="100")

    # Number of selected lineups per simulation
    parser.add_argument('-l', '--num_lineups', dest='num_lineups',
                        help='Number of lineups per simulation', default="3")

    args = parser.parse_args(sys.argv[1:])
    return {"num_simulations": int(args.num_simulations), "num_lineups": int(args.num_lineups)}


def read_json(path):
    return json.loads(read(path))


def read(path):
    with open(path, 'r') as f:
        return f.read()
