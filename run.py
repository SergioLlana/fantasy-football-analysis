from brkga.biwenger import run_simulation
import pandas as pd
import utils


def main():
    problem_config = utils.read_json("brkga/config/biwenger.json")
    config = utils.read_json("brkga/config/config.json")

    data = pd.read_csv("data/biwenger.csv", index_col=[0])
    data["value"] = data.value.str.replace(',', '').astype(int)

    for _ in range(10):
        run_simulation(data, problem_config, config)


if __name__ == "__main__":
    main()
