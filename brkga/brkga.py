from numpy.random import rand
import logging
import math


class Individual:
    def __init__(self, chromosome):
        self.chromosome = list(chromosome)
        self.fitness = None
        self.solution = {}


class BRKGA:
    def __init__(self, config):
        _logger = logging.getLogger(__name__)
        _logger.debug("BRKGA initialised")
        self.num_individuals = config["num_individuals"]
        self.inheritance_prob = config["inheritance_prob"]
        self.num_elite = int(math.ceil(self.num_individuals * config["elite_prop"]))
        self.num_mutants = int(math.ceil(self.num_individuals * config["mutant_prop"]))
        self.num_crossover = max(self.num_individuals - self.num_elite - self.num_mutants, 0)

    def init_population(self, chromosome_length):
        return [Individual(rand(chromosome_length)) for _ in range(self.num_individuals)]

    def classify_individuals(self, population):
        sorted_individuals = sorted(population, key=lambda x: x.fitness, reverse=True)
        elite = sorted_individuals[0:self.num_elite]
        non_elite = sorted_individuals[self.num_elite:self.num_individuals]
        return elite, non_elite

    def generate_mutants(self, chromosome_length):
        return [Individual(rand(chromosome_length)) for _ in range(self.num_mutants)]

    def do_crossover(self, elite, non_elite, chromosome_length):
        crossover = []
        for i in range(self.num_crossover):
            elite_idx = int(math.floor(rand() * len(elite)))
            non_elite_idx = int(math.floor(rand() * len(non_elite)))
            elite_chromosome = elite[elite_idx].chromosome
            non_elite_chromosome = non_elite[non_elite_idx].chromosome
            random = list(rand(chromosome_length))
            crossover.append(Individual(elite_chromosome[i]
                                        if random[i] <= self.inheritance_prob else non_elite_chromosome[i]
                                        for i in range(chromosome_length)))

        return crossover

    def best_individual(self, population):
        sorted_individuals = sorted(population, key=lambda x: x.fitness, reverse=True)
        return sorted_individuals[0]
