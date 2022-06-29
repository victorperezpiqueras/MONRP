import json

from evaluation.get_nondominated_solutions import get_nondominated_solutions
from evaluation.metrics import calculate_gdplus, calculate_unfr
from models.Solution import Solution

""" Please fill the experiments hyper-parameters, which will be used to define the which results
will be taken into account to find the reference Pareto for GD+ and UNFR"""

dependencies = ['True']  # {'True','False'}

# post metrics are not computed among results for all indicated datasets.Only 1 dataset is taken into account each time.
dataset = ['p1', 'a3', 'c3', 'c4', 'c5', 'c6'] # ['p1', 'p2', 'a1', 'a2', 'a3', 'a4', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6']
algorithm = 'feda'  # 'GRASP', 'geneticnds', 'nsgaii', 'umda', 'pbil', 'feda'

# COMMON HYPER-PARAMETERS #
# possible algorithm values: {'GRASP', 'feda', 'geneticnds', 'pbil', 'umda', nsgaii}
seed = 5
num_executions = 30
subset_size = [10]  # number of solutions to choose from final NDS in each algorithm to compute metrics
population_size = [100, 200, 500, 700, 1000]
num_generations = [50, 100, 200, 300, 400]
max_evals = [0]

# geneticNDS and NSGAii hyperparameters #
selection_candidates = [2]
crossover_prob = [0.8]
mutation_prob = [0.1, 0.3]  # [0.1, 0.3]
mutation = ['flip1bit']  # {'flip1bit', 'flipeachbit'}
replacement = ['elitismnds']  # {'elitism', 'elitismnds'}
selection = ['tournament']  # only 'tournament' available
crossover = ['onepoint']  # only 'onepoint' available

# GRASP hyper-parameters #
init_type = ['stochastically']  # {'stochastically', 'uniform'}
path_relinking_mode = ['None', 'after_local']  # {'None', 'after_local'}
local_search_type = ['best_first_neighbor_random']
# local_search_type values: {'None', 'best_first_neighbor_random','best_first_neighbor_sorted_score',
# best_first_neighbor_sorted_score_r' , 'best_first_neighbor_random_domination','best_first_neighbor_sorted_domination'}

# umda hyper-parameters #
selection_scheme = ['nds']  # {'nds','monoscore'}
replacement_scheme = ['elitism']  # {'elitism','replacement'}

# pbil hyper-parameters #
learning_rate = [0.1]
mutation_prob_pbil = [0.1]
mutation_shift = [0.1]

# feda hyper-parameters #
selection_scheme_feda = ['nds']  # {'nds','monoscore'}

''' returns a list of uid files created from geneticNDS hyper-parameters '''


def get_genetic_uids(name: str, d: str) -> [str]:
    uids_list = []

    for dependency in dependencies:
        for max_evalu in max_evals:
            for pop_size in population_size:
                for iterations in num_generations:
                    for sel in selection:
                        for xover in crossover:
                            for candidates in selection_candidates:
                                for xover_prob in crossover_prob:
                                    for mut_prob in mutation_prob:
                                        for mut in mutation:
                                            for rep in replacement:
                                                for size in subset_size:
                                                    uid_genetic = output_folder + name + dependency + d + \
                                                                  str(seed) + str(size) + str(pop_size) \
                                                                  + str(iterations) + str(max_evalu) + \
                                                                  str(candidates) + str(xover_prob) + str(mut_prob) + \
                                                                  sel + xover + mut + rep + str(num_executions) + \
                                                                  '.json'
                                                    print('\'../' + uid_genetic + '\',')
                                                    uids_list.append(uid_genetic)
    return uids_list


''' get_grasp_uids returns a list of uid files created from GRASP hyper-parameters '''


def get_grasp_uids(d: str) -> [str]:
    uids_list = []

    for dependency in dependencies:

        for max_evalu in max_evals:
            for pop_size in population_size:
                for iterations in num_generations:
                    for init in init_type:
                        for pr in path_relinking_mode:
                            for search in local_search_type:
                                for size in subset_size:
                                    uid_grasp = output_folder + 'GRASP' + dependency + d + str(seed) + str(size) + \
                                                str(iterations) + str(pop_size) + str(max_evalu) + init + search + \
                                                pr + str(num_executions) + '.json'
                                    print('\'../' + uid_grasp + '\',')
                                    uids_list.append(uid_grasp)
    return uids_list


''' returns a list of uid files created from umda hyper-parameters '''


def get_umda_uids(d: str) -> [str]:
    uids_list = []

    for dependency in dependencies:

        for max_evalu in max_evals:
            for pop_size in population_size:
                for iterations in num_generations:
                    for sel_scheme in selection_scheme:
                        for rep_scheme in replacement_scheme:
                            for size in subset_size:
                                uid_umda = output_folder + 'umda' + dependency + d + str(seed) + str(size) + \
                                           str(pop_size) + str(iterations) + str(max_evalu) + sel_scheme + \
                                           rep_scheme + str(num_executions) + '.json'
                                print('\'../' + uid_umda + '\',')
                                uids_list.append(uid_umda)
    return uids_list


''' returns a list of uid files created from pbil hyper-parameters '''


def get_pbil_uids(d: str) -> [str]:
    uids_list = []

    for dependency in dependencies:

        for max_evalu in max_evals:
            for pop_size in population_size:
                for iterations in num_generations:
                    for l_rate in learning_rate:
                        for mut_prob_pbil in mutation_prob_pbil:
                            for shift in mutation_shift:
                                for size in subset_size:
                                    uid_pbil = output_folder + 'pbil' + dependency + d + str(seed) + str(size) + \
                                               str(pop_size) + \
                                               str(iterations) + str(max_evalu) + str(l_rate) + str(mut_prob_pbil) + \
                                               str(shift) + str(num_executions) + '.json'
                                    print('\'../' + uid_pbil + '\',')
                                    uids_list.append(uid_pbil)
    return uids_list


''' returns a list of uid files created from feda hyper-parameters '''


def get_feda_uids(d: str) -> [str]:
    uids_list = []

    for dependency in dependencies:

        for max_evalu in max_evals:
            for pop_size in population_size:
                for iterations in num_generations:
                    for sel_scheme in selection_scheme_feda:
                        for size in subset_size:
                            uid_feda = output_folder + 'feda' + dependency + d + str(seed) + str(size) + \
                                       str(pop_size) + \
                                       str(iterations) + str(max_evalu) + sel_scheme + str(num_executions) + '.json'

                            print('\'../' + uid_feda + '\',')
                            uids_list.append(uid_feda)
    return uids_list


def construct_store_reference_pareto(uids):
    # construct reference Pareto, to be used to calculate UNFR and GD+. It is constructed with the non dominated
    # solutions among all nds together from all experiments with hyperparameters depicted above

    # construct reference pareto front
    all_solutions = []
    for file in uids:
        try:
            with open(file, 'r') as f_temp:
                dictio = json.load(f_temp)
                paretos = dictio['paretos']
                for pareto in paretos:
                    for xy in pareto:
                        sol = Solution(dataset=None, probabilities=None, uniform=None,
                                       cost=xy[0], satisfaction=xy[1])
                        all_solutions.append(sol)
        except (FileNotFoundError, IOError):
            print("File not found so not used to extract metrics: ", file)

    nds = get_nondominated_solutions(solutions=all_solutions)
    # print(f"Reference Pareto contains {len(nds)} solutions.")
    pareto = []
    for sol in nds:
        pareto.append([sol.total_cost, sol.total_satisfaction])

    # store reference pareto front
    for file in uids:
        try:
            with open(file, 'r') as f_temp:
                dictio = json.load(f_temp)
                dictio['Reference_Pareto'] = pareto
            with open(file, 'w') as f_temp:
                json.dump(dictio, f_temp, ensure_ascii=False, indent=4)
        except (FileNotFoundError, IOError):
            pass

    return pareto


# for each pareto in each file in files_uid, compute and store gd_plus respect to reference pareto front
def compute_and_store_gdplus(rpf, uids):
    for file in uids:
        try:
            with open(file, 'r') as file_without_gd:
                dictio = json.load(file_without_gd)
                paretos = dictio['paretos']
                gd_plus = []
                for pareto in paretos:
                    gd_plus.insert(len(gd_plus), calculate_gdplus(pareto, rpf))
                    metrics = dictio['metrics']
                metrics['gdplus'] = gd_plus
            with open(file, 'w') as file_with_gd:
                json.dump(dictio, file_with_gd, ensure_ascii=False, indent=4)
        except (FileNotFoundError, IOError):
            pass


# for each pareto in each file in files_uid, compute and store unfr respect to reference pareto front
def compute_and_store_unfr(rpf, uids):
    for file in uids:
        try:
            with open(file, 'r') as f_temp:
                dictio = json.load(f_temp)
                paretos = dictio['paretos']
                unfr = []
                for pareto in paretos:
                    unfr.insert(len(unfr), calculate_unfr(pareto, rpf))
                    metrics = dictio['metrics']
                metrics['unfr'] = unfr
            with open(file, 'w') as f_temp:
                json.dump(dictio, f_temp, ensure_ascii=False, indent=4)
        except (FileNotFoundError, IOError):
            pass


if __name__ == '__main__':
    print('GD+ and UNFR will be calculated using as reference the best pareto found in the output files given + \
                 the hyperparameters, for each dataset.')
    output_folder = "output/" + algorithm + '/'  # folder with output files from which to extract
    all_files_uid = []
    for data in dataset:

        files_uid = []
        # find unique file ids from the list of hyperparameters set at the beginning of this file, above.
        if 'GRASP' == algorithm:
            files_uid = files_uid + get_grasp_uids(data)
        if 'geneticnds' == algorithm:
            files_uid = files_uid + get_genetic_uids('geneticNDS', data)
        if 'nsgaii' == algorithm:
            files_uid = files_uid + get_genetic_uids('nsgaii', data)
        if 'umda' == algorithm:
            files_uid = files_uid + get_umda_uids(data)
        if 'pbil' == algorithm:
            files_uid = files_uid + get_pbil_uids(data)
        if 'feda' == algorithm:
            files_uid = files_uid + get_feda_uids(data)

        # find Reference Pareto and compute metrics
        reference_pareto = construct_store_reference_pareto(files_uid)
        try:
            compute_and_store_gdplus(rpf=reference_pareto, uids=files_uid)
        except:
            print("en compute_and_store_gdplus")

        try:
            compute_and_store_unfr(rpf=reference_pareto, uids=files_uid)
        except:
            print("en compute_and_store_unfr ")

        print()
        for f in files_uid:
            all_files_uid.append(f)

    # store all uids in container file (for use in analysis jupyter notebook)
    container_name = 'filest_list_' + algorithm
    with open('output/' + container_name, 'w') as container_file:
        for uid in all_files_uid:
            container_file.write(uid + "\n")
