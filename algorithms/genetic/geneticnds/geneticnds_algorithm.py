from algorithms.abstract_default.evaluation_exception import EvaluationLimit
from algorithms.genetic.abstract_genetic.basegenetic_algorithm import BaseGeneticAlgorithm
from algorithms.genetic.geneticnds.geneticnds_executer import GeneticNDSExecuter
from algorithms.genetic.geneticnds.geneticnds_utils import GeneticNDSUtils
import copy
import time


class GeneticNDSAlgorithm(BaseGeneticAlgorithm):
    def __init__(self, dataset_name="1", random_seed=None, population_length=20, max_generations=1000,max_evaluations=0,
                 selection="tournament", selection_candidates=2,
                 crossover="onepoint", crossover_prob=0.9,
                 mutation="flipeachbit", mutation_prob=0.1,
                 replacement="elitism"):

        self.utils = GeneticNDSUtils(
            random_seed, population_length, selection_candidates, crossover_prob, mutation_prob)
        self.executer = GeneticNDSExecuter(algorithm=self)
        self.problem, self.dataset = self.utils.generate_dataset_problem(
            dataset_name=dataset_name)
        self.dataset_name = dataset_name

        self.population_length = population_length
        self.max_generations = max_generations
        self.max_evaluations = max_evaluations
        self.random_seed = random_seed

        self.selection_scheme = selection
        self.selection_candidates = selection_candidates
        self.crossover_scheme = crossover
        self.crossover_prob = crossover_prob
        self.mutation_scheme = mutation
        self.mutation_prob = mutation_prob
        self.replacement_scheme = replacement

        self.best_individual = None
        self.population = None
        self.best_generation_avgValue = None
        self.best_generation = None
        self.nds = []
        self.num_evaluations = 0
        self.num_generations = 0

        #self.evaluate = self.utils.evaluate
        self.calculate_last_generation_with_enhance = self.utils.calculate_last_generation_with_enhance
        self.generate_starting_population = self.utils.generate_starting_population

        if selection == "tournament":
            self.selection = self.utils.selection_tournament

        if crossover == "onepoint":
            self.crossover = self.utils.crossover_one_point

        if mutation == "flip1bit":
            self.mutation = self.utils.mutation_flip1bit
        elif mutation == "flipeachbit":
            self.mutation = self.utils.mutation_flipeachbit

        if replacement == "elitism":
            self.replacement = self.utils.replacement_elitism
        elif replacement == "elitismnds":
            self.replacement = self.utils.replacement_elitism

        self.file = str(self.__class__.__name__)+"-"+str(dataset_name)+"-"+str(random_seed)+"-"+str(population_length)+"-" +\
            str(max_generations)+ "-"+str(max_evaluations)+"-"+selection+"-"+str(selection_candidates)+"-" +\
            str(crossover)+"-"+str(crossover_prob)+"-"+str(mutation) + \
            "-"+str(mutation_prob)+"-"+str(replacement)+".txt"

    def get_name(self):
        return "GeneticNDS+"+str(self.population_length)+"+"+str(self.max_generations)+ \
            + "+"+str(self.max_evaluations)+"+"+str(self.crossover_prob)\
            + "+"+str(self.mutation_scheme)+"+"+str(self.mutation_prob)


    # UPDATE NDS------------------------------------------------------------------
    def is_non_dominated(self, ind, nds):
        non_dominated = True
        for other_ind in nds:
            # if ind.dominates(other_ind):
            # non_dominated=non_dominated and True
            #	pass
            # elif other_ind.dominates(ind):
            if other_ind.dominates(ind):
                non_dominated = False
                break

        return non_dominated

    def updateNDS(self, new_population):
        new_nds = []
        merged_population = copy.deepcopy(self.nds)
        merged_population.extend(new_population)
        for ind in merged_population:
            dominated = False
            for other_ind in merged_population:
                if other_ind.dominates(ind):
                    dominated = True
                    break
            if not dominated:
                new_nds.append(ind)
        new_nds = list(set(new_nds))
        self.nds = copy.deepcopy(new_nds)

    def evaluate(self, population, best_individual):
        #super().evaluate(population, best_individual)
        try:
            best_score = 0
            new_best_individual = None
            for ind in population:
                ind.evaluate_fitness()
                self.add_evaluation(population)#############
                if ind.total_score > best_score:
                    new_best_individual = copy.deepcopy(ind)
                    best_score = ind.total_score
            if best_individual is not None:
                if new_best_individual.total_score > best_individual.total_score:
                    best_individual = copy.deepcopy(new_best_individual)
            else:
                best_individual = copy.deepcopy(new_best_individual)
        except EvaluationLimit:
            pass


    def add_evaluation(self,new_population):
        self.num_evaluations+=1
        #if(self.num_evaluations >= self.max_evaluations):
        if (self.stop_criterion(self.num_generations, self.num_evaluations)):
            self.updateNDS(new_population)
            raise EvaluationLimit


    def reset(self):
        self.nds = []
        self.best_generation_avgValue = 0
        self.best_generation = 0
        self.num_evaluations = 0
        self.num_generations = 0
        self.best_individual = None
        self.population = None


    # RUN ALGORITHM------------------------------------------------------------------
    def run(self):
        self.reset()
        start = time.time()
        
        self.num_generations = 0
        self.num_evaluations = 0
        self.population = self.generate_starting_population()
        self.evaluate(self.population, self.best_individual)
        # print("Best individual score: ", self.best_individual.total_score)

        # or not(num_generations > (self.best_generation+20)):
        #while (num_generations < self.max_generations):
        try:
            while (not self.stop_criterion(self.num_generations, self.num_evaluations)):
                # selection
                new_population = self.selection(self.population)
                # crossover
                new_population = self.crossover(new_population)

                # mutation
                new_population = self.mutation(new_population)

                # evaluation
                self.evaluate(self.population, self.best_individual)
                #num_evaluations+=len(self.population)

                # update NDS
                self.updateNDS(new_population)

                returned_population = copy.deepcopy(new_population)
                self.best_generation, self.best_generation_avgValue = self.calculate_last_generation_with_enhance(
                    self.best_generation, self.best_generation_avgValue, self.num_generations, returned_population)

                # replacement
                if self.replacement_scheme == "elitismnds":
                    self.population = self.replacement(self.nds, new_population)
                else:
                    self.population = self.replacement(
                        self.population, new_population)

                self.num_generations += 1
                # mostrar por pantalla
                # if num_generations % 100 == 0:
                # print("Nº Generations: ", num_generations)
                # print("Best individual score: ", self.best_individual.total_score)
            
        except EvaluationLimit:
            pass

        # end
        # print(self.best_individual)
        end = time.time()

        return {  # "population": returned_population,
            "population": self.nds,
            "time": end - start,
            "best_individual": self.best_individual,
            # "nds": self.nds,
            "bestGeneration": self.best_generation,
            "numGenerations": self.num_generations,
            "numEvaluations": self.num_evaluations
        }
