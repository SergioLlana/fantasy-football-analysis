import argparse
import json
import csv
import sys


def read_json(path):
    return json.loads(read(path))


def read(path):
    with open(path, 'r') as f:
        return f.read()


def write_line(path, line):
    with open(path, 'a') as f:
        f.write_line(line)


def write_csv(path, content):
    with open(path, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(content)


def parse_market_scraper_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--headless', dest='headless', help='Headless', action='store_true', default=False)
    parser.add_argument('-l', '--league_index', dest='league_index', help='League index', default="1")
    parser.add_argument('-p', '--start_page', dest='start_page', help='Start page', default="1")

    args = parser.parse_args(sys.argv[1:])
    return {"league_index": int(args.league_index), "start_page": int(args.start_page), "headless": args.headless}


def parse_team_scraper_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--headless', dest='headless', help='Headless', action='store_true', default=False)
    parser.add_argument('-l', '--league_index', dest='league_index', help='League index', default="1")

    args = parser.parse_args(sys.argv[1:])
    return {"league_index": int(args.league_index), "headless": args.headless}