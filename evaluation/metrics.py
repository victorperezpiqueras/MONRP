import math
from typing import List
import numpy as np
from datasets.Dataset import Dataset
from pymoo.factory import get_performance_indicator
from pymoo.visualization.scatter import Scatter
from models.Solution import Solution


def calculate_avgValue(population: List[Solution]) -> float:
    avgValue = 0
    for ind in population:
        avgValue += ind.compute_mono_objective_score()
    avgValue /= len(population)
    return avgValue


def calculate_bestAvgValue(population: List[Solution]) -> float:
    bestAvgValue = 0
    for ind in population:
        if bestAvgValue < ind.compute_mono_objective_score():
            bestAvgValue = ind.compute_mono_objective_score()

    return bestAvgValue


def calculate_numSolutions(population: List[Solution]) -> int:
    return len(set(population))


def calculate_spacing(population: List[Solution]) -> float:
    n = len(population)
    N = 2
    spacing = 0
    mean_objectives = []

    objective = 0
    for j in range(0, len(population)):
        objective += population[j].total_cost
    objective /= len(population)
    mean_objectives.append(objective)

    objective = 0
    for j in range(0, len(population)):
        objective += population[j].total_satisfaction
    objective /= len(population)
    mean_objectives.append(objective)

    for j in range(0, len(population)):
        aux_spacing = 0
        for i in range(0, N):
            di = mean_objectives[i]
            if i == 0:
                dij = population[j].total_cost
            elif i == 1:
                dij = population[j].total_satisfaction
            aux = (1 - (abs(dij) / di)) ** 2
            aux_spacing += aux
        aux_spacing = math.sqrt(aux_spacing)
        spacing += aux_spacing

    spacing /= (n * N)
    return spacing



def calculate_hypervolume_old(population: List[Solution]) -> float:
    objectives_diff = []
    aux_max_cost, aux_max_sat = population[0].get_max_cost_satisfactions()
    aux_min_cost, aux_min_sat = population[0].get_min_cost_satisfactions()

    aux_min = float('inf')
    aux_max = 0
    for ind in population:
        if ind.total_cost < aux_min:
            aux_min = ind.total_cost
        if ind.total_cost > aux_max:
            aux_max = ind.total_cost
    aux_max_norm = (aux_max-aux_min_cost)/(aux_max_cost-aux_min_cost)
    aux_min_norm = (aux_min-aux_min_cost)/(aux_max_cost-aux_min_cost)
    aux_val = aux_max_norm-aux_min_norm
    objectives_diff.append(aux_val)

    aux_min = float('inf')
    aux_max = 0
    for ind in population:
        if ind.total_satisfaction < aux_min:
            aux_min = ind.total_satisfaction
        if ind.total_satisfaction > aux_max:
            aux_max = ind.total_satisfaction
    aux_max_norm = (aux_max-aux_min_sat)/(aux_max_sat-aux_min_sat)
    aux_min_norm = (aux_min-aux_min_sat)/(aux_max_sat-aux_min_sat)
    aux_val = aux_max_norm-aux_min_norm
    objectives_diff.append(aux_val)

    hypervolume = 1
    for i in range(0, len(objectives_diff)):
        hypervolume *= objectives_diff[i]

    return hypervolume

def calculate_hypervolume(population: List[Solution]) -> float:

    points = []
    nadir_x = float("-inf")
    nadir_y = float("-inf")
    best_x = float("+inf")
    best_y = float("+inf")

    for ind in population:
        #se revierte el orden, más es peor, para compatibilidad con pymoo
        x = 1 - ind.total_cost
        y = 1 - ind.total_satisfaction
        points.append([x, y])
        nadir_x = x if x > nadir_x else nadir_x
        nadir_y = y if y > nadir_y else nadir_y
        best_x = x if x < best_x else best_x
        best_y = y if y < best_y else best_y
    np_points = np.array(points)
    range_x = nadir_x - best_x
    range_y = nadir_y - best_y

    ref_x = nadir_x + range_x/10
    ref_y = nadir_y + range_y / 10
    ref_x = 1 if ref_x > 1 else ref_x
    ref_y = 1 if ref_y > 1 else ref_y

    Scatter().add(np_points).show()

    hv = get_performance_indicator("hv", ref_point=np.array(np.array([ref_x, ref_y])))
    hypervolume = hv.do(np_points)
    print(hypervolume)
    return hypervolume



def eudis2(v1: float, v2: float) -> float:
    return math.dist(v1, v2)
    # return distance.euclidean(v1, v2)


def calculate_spread(population: List[Solution]) -> float:

    dataset: Dataset = population[0].dataset

    MIN_OBJ1 = 0
    MIN_OBJ2 = 0

    MAX_OBJ1 = np.max(dataset.pbis_satisfaction_scaled)
    MAX_OBJ2 = np.max(dataset.pbis_cost_scaled)

    df = None
    dl = None
    davg = None
    sum_dist = None
    N = len(population)
    spread = None

    first_solution = population[0]
    last_solution = population[len(population) - 1]

    first_extreme = [MIN_OBJ1, MIN_OBJ2]
    last_extreme = [MAX_OBJ1, MAX_OBJ2]

    df = eudis2([first_solution.total_satisfaction,
                first_solution.total_cost], first_extreme)
    dl = eudis2([last_solution.total_satisfaction,
                last_solution.total_cost], last_extreme)

    davg = 0
    dist_count = 0
    for i in range(0, len(population)):
        for j in range(0, len(population)):
            # avoid distance from a point to itself
            if i != j:
                dist_count += 1
                davg += eudis2([population[i].total_satisfaction, population[i].total_cost],
                               [population[j].total_satisfaction, population[j].total_cost])
    davg /= dist_count

    # calculate sumatory(i=1->N-1) |di-davg|
    sum_dist = 0
    for i in range(0, len(population) - 1):
        di = eudis2([population[i].total_satisfaction, population[i].total_cost],
                    [population[i + 1].total_satisfaction, population[i + 1].total_cost])
        sum_dist += abs(di - davg)

    # spread formula
    spread = (df + dl + sum_dist) / (df + dl + (N - 1) * davg)
    return spread


def calculate_mean_bits_per_sol(solutions: List[Solution]) -> float:
    genes = 0
    n_sols = len(solutions)
    for sol in solutions:
        genes += np.count_nonzero(sol.selected)
    return genes/n_sols
