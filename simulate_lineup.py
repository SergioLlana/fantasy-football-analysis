from brkga.biwenger import run_simulation
import pandas as pd
import logging
from utils import parse_simulator_args, read_json


def simulate(args):
    problem_config = read_json("brkga/config/biwenger.json")
    config = read_json("brkga/config/config.json")

    data = pd.read_csv("data/players.csv", index_col=[0])
    data["value"] = data.value.str.replace(',', '').astype(int)

    teams = []
    for i in range(args["num_simulations"]):
        best_teams_info = run_simulation(data, problem_config, config, args["num_lineups"])
        logging.info("Simulation {0} out of {1} done.".format(i, args["num_simulations"]))

        for team_info in best_teams_info:
            lineup = [team_info["goalkeepers"], team_info["defenders"],
                      team_info["midfielders"], team_info["forwards"]]

            logging.info([player for line in lineup for player in line])
            teams.append(team_info)

    pd.DataFrame(teams).to_csv("data/lineups.csv", sep=";")


if __name__ == "__main__":
    args = parse_simulator_args()

    console = logging.StreamHandler()
    console.setLevel("INFO")
    console.setFormatter(logging.Formatter("%(message)s"))
    logging.getLogger("").addHandler(console)

    logging.info("STARTING LINEUP SIMULATOR")

    simulate(args)

    logging.info("PROCESS FINISHED")

