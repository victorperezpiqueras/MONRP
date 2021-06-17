def generate_configurations():
    # grasp grasp 1 5 10 10 best_first_neighbor
    # opciones------------------------------------------------------------------
    dataset_problems = [
        "1",
        "2"
    ]
    algorithms = [
        "grasp"
    ]
    iterations = [
        20, 50, 100, 200, 300, 500, 1000
    ]
    solutions_per_iteration_list = [
        20, 40, 60, 80, 100, 200, 500, 1000
    ]
    init_types=["stochastically","uniform"]
    local_search_types = [
        #"best_first_neighbor",
        #"best_first_neighbor_random",
        #"best_first_neighbor_sorted_score",
        "best_first_neighbor_sorted_score_r",
    ]
    seed = 10

    f = open("configs.txt", "w")
    returnStr = ''
    type = "grasp"
    for dataset_problem in dataset_problems:
        for algorithm in algorithms:
            for iteration in iterations:
                for solutions_per_iteration in solutions_per_iteration_list:
                    for init_type in init_types:
                        for local_search_type in local_search_types:
                            returnStr = type + ' ' + str(algorithm) + " " + str(dataset_problem) + ' ' + \
                                str(seed) + ' ' + str(iteration) + ' ' + \
                                str(solutions_per_iteration) + ' ' + \
                                str(init_type) + ' ' + \
                                str(local_search_type) + '\n'
                            f.write(returnStr)
    f.close()


generate_configurations()
