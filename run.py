from brkga.biwenger import run_simulation
import pandas as pd
import utils


def main():
    problem_config = utils.read_json("brkga/config/biwenger.json")
    config = utils.read_json("brkga/config/config.json")

    data = pd.read_csv("data/biwenger.csv", index_col=[0])
    data["value"] = data.value.str.replace(',', '').astype(int)

    teams = []
    num_simulations = 100
    for i in range(num_simulations):
        best_team_info = run_simulation(data, problem_config, config)
        lineup = [best_team_info["goalkeepers"], best_team_info["defenders"],
                  best_team_info["midfielders"], best_team_info["forwards"]]

        print("Simulation {0} out of {1} done.".format(i, num_simulations))
        print([player for line in lineup for player in line])

        teams.append(best_team_info)
    pd.DataFrame(teams).to_csv("data/lineups.csv", sep=";")


if __name__ == "__main__":
    main()
