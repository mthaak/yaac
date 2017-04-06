import csv
import traceback
from itertools import zip_longest

from src.alg.ACO import *
from src.alg.ASRanked import *
from src.alg.EAS2 import *
from src.alg.MINMAX import *
from src.map.Map import Map

# Initialization
map = Map()
map_names = ['initMap', 'smallMap', 'mediumMap', 'largeMap']
alg_names = ['ACO', 'ASRanked', 'EAS', 'MINMAX']

# Set parameters here
MAX_ITERATIONS = 20000
ALPHA_BETA_STEP = 0.5
ITERATIONS_STEP = 10
NR_TESTS = 10


# http://stackoverflow.com/questions/477486/how-to-use-a-decimal-range-step-value
def drange(start, stop, step):
    r = start
    while r < stop:
        yield r
        r += step


def get_optimal_path(map_nr, home_pos, food_pos):
    """Returns the optimal path for a given map, home location and food location. Hardcoded."""
    if map_nr == 0:
        return 13
    elif map_nr == 1:
        return 14
    elif map_nr == 2:
        # Optimal for respectively (2, 13), (3, 8), (13, 2), and (13, 13)
        if food_pos == (2, 13) or food_pos == (3, 8):
            return 15
        elif food_pos == (13, 2):
            return 19
        elif food_pos == (13, 13):
            return 24
    elif map_nr == 3:
        # Optimal for respectively (3, 18), (14, 13), (18, 18)
        if food_pos == (3, 18) and home_pos == (1, 1):
            return 19
        elif food_pos == (15, 12) and home_pos == (1, 1):
            return 27
        elif food_pos == (18, 18) and home_pos == (1, 1):
            return 34
        elif food_pos == (16, 3) and home_pos == (1, 1):
            return 21
        elif food_pos == (3, 18) and home_pos == (4, 17):
            return 2
        elif food_pos == (15, 12) and home_pos == (4, 17):
            return 38
        elif food_pos == (18, 18) and home_pos == (4, 17):
            return 39
        elif food_pos == (16, 3) and home_pos == (4, 17):
            return 36
    return 0


def calc_optimal_path(map_nr, home_pos):
    food_list = [prop for prop in map.getProps() if prop.model in PropModel.food()]
    return min([get_optimal_path(map_nr, home_pos, (food.i, food.j)) for food in food_list])


def calc_nr_entities_optimal_path(entities):
    """Returns the number of entities that has found the optimal path from their home to some food."""
    return sum([entity.best_path == get_optimal_path(map_nr, entity.home_pos, entity.food_pos) for entity in entities])


def run_test(map_nr, alg_nr, alpha=1.0, beta=1.0, pheromone=1, max_iterations=10000):
    # Set map and algorithm
    map.setMap(map_nr)
    if alg_nr == 0:
        alg = ACO(map)
    elif alg_nr == 1:
        alg = ASRanked(map)
    elif alg_nr == 2:
        alg = EAS2(map)
    elif alg_nr == 3:
        alg = MINMAX(map)

    entities = alg.getEntities()

    # Set entity parameters
    for entity in entities:
        entity.alpha = alpha
        entity.beta = beta
        entity.pherodrop = pheromone

    avg_best_paths = [entities[0].best_path]  # list of average best paths per ITERATIONS_STEP

    # Perform iterations
    iterations = 0
    while calc_nr_entities_optimal_path(entities) < len(entities) and iterations < max_iterations:
        alg.update()
        iterations += 1
        if iterations % ITERATIONS_STEP == 0:
            avg_best_path = sum([entity.best_path for entity in entities]) / len(entities)
            avg_best_paths.append(avg_best_path)

    # Write last ITERATION_STEP as well
    if iterations < max_iterations:
        temp_iterations = iterations
        while temp_iterations % ITERATIONS_STEP != 0:
            alg.update()
            temp_iterations += 1
        avg_best_path = sum([entity.best_path for entity in entities]) / len(entities)
        avg_best_paths.append(avg_best_path)

    nr_entities_optimal_path = calc_nr_entities_optimal_path(entities)
    optimal_path = calc_optimal_path(map_nr, entities[0].home_pos)  # all entities have same home pos
    return iterations, avg_best_paths, nr_entities_optimal_path, optimal_path


with open('results.csv', 'w', newline='') as results_file:
    writer = csv.writer(results_file, delimiter=',')

    writer.writerow(['map', 'alg', 'alpha', 'beta', 'pheromone', 'opt_path',
                     'iterations_mean', 'iterations_std',
                     'best_path_mean', 'best_path_std',
                     'nr_entities_best_path_mean', 'nr_entities_best_path_std'])

    alpha, beta, pheromone = 1, 1, 1

    for map_nr, map_name in enumerate(map_names):
        for alg_nr, alg_name in enumerate(alg_names):
            if alg_nr != 0:
                continue
            for alpha in drange(0, 2.0, ALPHA_BETA_STEP):
                beta = 2.0 - alpha
                iterations_list, best_paths_list, nr_entities_optimal_path_list, optimal_path = [], [], [], 0
                for test_nr in range(NR_TESTS):
                    print('Running test: {0}, {1}, {2} ... '.format(map_name, alg_name, test_nr), end='')
                    try:
                        iterations, best_paths, nr_entities_optimal_path, optimal_path = run_test(map_nr, alg_nr,
                                                                                                  max_iterations=MAX_ITERATIONS,
                                                                                                  alpha=alpha,
                                                                                                  beta=beta)
                        iterations_list.append(iterations)
                        best_paths_list.append(best_paths)
                        nr_entities_optimal_path_list.append(nr_entities_optimal_path)
                        print('success ({0} iterations)'.format(iterations))
                    except Exception as err:
                        print('failed: ')
                        print(traceback.format_exc())

                best_path_list = [best_paths[-1] for best_paths in best_paths_list]

                # Write averages and standard deviations
                writer.writerow([map_name, alg_name, round(alpha, 1), round(beta, 1), pheromone, optimal_path,
                                 round(np.mean(iterations_list), 5), round(np.std(iterations_list), 5),
                                 round(np.mean(best_path_list), 5), round(np.std(best_path_list), 5),
                                 round(np.mean(nr_entities_optimal_path_list), 5),
                                 round(np.std(nr_entities_optimal_path_list), 5)])

                if alpha == 1.0:  # only write when alpha = beta = 1.0
                    # Write specific map x alg file with best_path per ITERATIONS_STEP
                    file_name = map_name + '_' + alg_name + '.csv'
                    with open(file_name, 'w', newline='') as best_path_file:
                        writer2 = csv.writer(best_path_file, delimiter=',')
                        writer2.writerow(['iterations', 'avg_best_path_mean', 'avg_best_path_std'])
                        for iteration, avg_best_path_per_iter in enumerate(zip_longest(*best_paths_list)):
                            avg_best_path_per_iter_no_none = [best_path if best_path else optimal_path for best_path in
                                                              avg_best_path_per_iter]
                            writer2.writerow([str(iteration * ITERATIONS_STEP),
                                              round(np.mean(avg_best_path_per_iter_no_none), 5),
                                              round(np.std(avg_best_path_per_iter_no_none), 5)])
