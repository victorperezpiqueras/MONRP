from algorithms.genetic.abstract_genetic.genetic_executer import GeneticExecuter


class GeneticNDSExecuter(GeneticExecuter):
    def __init__(self, algorithm):
        super().__init__(algorithm)
        self.algorithm_type = "genetic_nds"
