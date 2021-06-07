import evaluation.metrics as metrics
from algorithms.abstract_default.executer import Executer


class GRASPExecuter(Executer):
    def __init__(self, algorithm):
        self.algorithm_type = "grasp"
        self.algorithm = algorithm

    def initialize_file(self, file_path):
        # print("Running...")
        f = open(file_path, "w")
        f.write("Dataset,Algorithm,Iterations,Solutions per Iteration,"
                "Local Search Type,Time(s),AvgValue,BestAvgValue,HV,Spread,NumSolutions,Spacing\n")
        f.close()

    def reset_file(self, file_path):
        file = open(file_path, "w")
        file.close()

    def execute(self, executions, file_path):
        algorithm_name = self.algorithm.__class__.__name__
        dataset = self.algorithm.dataset_name
        iterations = self.algorithm.iterations
        solutions_per_iteration = self.algorithm.solutions_per_iteration
        local_search_type = self.algorithm.local_search_type

        for i in range(0, executions):
            #print("Executing iteration: ", i + 1)
            result = self.algorithm.run()

            time = str(result["time"]) if "time" in result else 'NaN'
            numGenerations = str(
                result["numGenerations"]) if "numGenerations" in result else 'NaN'

            avgValue = str(metrics.calculate_avgValue(result["population"]))
            bestAvgValue = str(metrics.calculate_bestAvgValue(result["population"]))
            hv = str(metrics.calculate_hypervolume(result["population"]))
            spread = str(metrics.calculate_spread(result["population"]))
            numSolutions = str(metrics.calculate_numSolutions(result["population"]))
            spacing = str(metrics.calculate_spacing(result["population"]))

            f = open(file_path, "a")
            data = str(dataset) + "," + \
                str(algorithm_name) + "," + \
                str(iterations) + "," + \
                str(solutions_per_iteration) + "," + \
                str(local_search_type) + "," + \
                str(time) + "," + \
                str(avgValue) + "," + \
                str(bestAvgValue) + "," + \
                str(hv) + "," + \
                str(spread) + "," + \
                str(numSolutions) + "," + \
                str(spacing) + "," + \
                str(numGenerations) + \
                "\n"

            f.write(data)
            f.close()

        # print("End")