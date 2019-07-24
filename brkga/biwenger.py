from brkga.brkga import BRKGA
import math


def run_simulation(players_df, lineup_config, brkga_config):
    problem = Problem(lineup_config, players_df)
    brkga = BRKGA(brkga_config)
    decoder = Decoder(problem)

    chromosome_length = decoder.num_genes
    population = brkga.init_population(chromosome_length)

    for _ in range(brkga_config["num_generations"]):
        population = decoder.decode(population)
        mutants = brkga.generate_mutants(chromosome_length)
        elite, non_elite = brkga.classify_individuals(population)
        crossover = brkga.do_crossover(elite, non_elite, chromosome_length)
        population = elite + crossover + mutants

    population = decoder.decode(population)
    best_individual = brkga.best_individual(population)

    selected_players = players_df.loc[players_df.index.isin(best_individual.solution.selected_players)]
    goalkeepers = selected_players.loc[selected_players["position"] == "Goalkeeper"]
    defenders = selected_players.loc[selected_players["position"] == "Defender"]
    midfielders = selected_players.loc[selected_players["position"] == "Midfielder"]
    forwards = selected_players.loc[selected_players["position"] == "Forward"]

    return {
        "goalkeepers": goalkeepers.name.tolist(),
        "goalkeeper_points": goalkeepers.points.tolist(),
        "goalkeeper_values": goalkeepers.value.tolist(),
        "defenders": defenders.name.tolist(),
        "defender_points": defenders.points.tolist(),
        "defender_values": defenders.value.tolist(),
        "midfielders": midfielders.name.tolist(),
        "midfielder_points": midfielders.points.tolist(),
        "midfielder_values": midfielders.value.tolist(),
        "forwards": forwards.name.tolist(),
        "forward_points": forwards.points.tolist(),
        "forward_values": forwards.value.tolist(),
        "total_value": selected_players.value.sum(),
        "total_points": best_individual.fitness
    }


class Problem(object):
    def __init__(self, config, data):
        self.data = data
        self.config = config

        self.money = config["money"]
        self.num_forwards = config["num_forwards"]
        self.num_defenders = config["num_defenders"]
        self.num_midfielders = config["num_midfielders"]
        self.num_goalkeepers = config["num_goalkeepers"]
        self.num_players = (self.num_forwards + self.num_midfielders + self.num_defenders + self.num_goalkeepers)

        self.available_players = data.loc[(data.games > 15) & (~data["name"].isin(config["player_blacklist"]))]
        self.goalkeepers = self.available_players.loc[self.available_players.position == "Goalkeeper"].reset_index(level=0)
        self.defenders = self.available_players.loc[self.available_players.position == "Defender"].reset_index(level=0)
        self.midfielders = self.available_players.loc[self.available_players.position == "Midfielder"].reset_index(level=0)
        self.forwards = self.available_players.loc[self.available_players.position == "Forward"].reset_index(level=0)


class Solution(Problem):
    def __init__(self, config, data):
        super(Solution, self).__init__(config, data)
        self.selected_players = []

    @staticmethod
    def create_empty_solution(problem):
        solution = Solution(problem.config, problem.data)
        return solution

    def calculate_fitness(self):
        selected_players = self.available_players.loc[self.available_players.index.isin(self.selected_players)]

        if len(self.selected_players) != len(set(self.selected_players)):
            return 0

        if sum(selected_players.value) >= self.money:
            return 0

        return selected_players.points.sum()


class Decoder:
    def __init__(self, problem):
        self.num_genes = problem.num_players
        self.problem = problem

    def decode(self, population):
        for individual in population:
            solution, fitness = self._decode_individual(individual)
            individual.solution = solution
            individual.fitness = fitness
        return population

    def _decode_individual(self, individual):
        gk = self.problem.num_goalkeepers
        df = gk + self.problem.num_defenders
        md = gk + df + self.problem.num_midfielders
        solution = Solution.create_empty_solution(self.problem)

        for idx, gene in enumerate(individual.chromosome):
            if idx < gk:
                num_goalkeepers = self.problem.goalkeepers.shape[0]
                player_idx = self.problem.goalkeepers.iloc[int(math.floor(num_goalkeepers * gene))]["index"]
            elif idx < df:
                num_defenders = self.problem.defenders.shape[0]
                player_idx = self.problem.defenders.iloc[int(math.floor(num_defenders * gene))]["index"]
            elif idx < md:
                num_midfielders = self.problem.midfielders.shape[0]
                player_idx = self.problem.midfielders.iloc[int(math.floor(num_midfielders * gene))]["index"]
            else:
                num_forwards = self.problem.forwards.shape[0]
                player_idx = self.problem.forwards.iloc[int(math.floor(num_forwards * gene))]["index"]
            solution.selected_players.append(player_idx)

        return solution, solution.calculate_fitness()
