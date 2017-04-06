from src.alg.ASRanked import *
from src.map.Map import Map
from src.alg.ACO import *
from src.alg.EAS2 import *
from src.alg.MINMAX import *
import csv

# Initialization
map = Map()
alg1 = ACO(map)
alg2 = ASRanked(map)
alg3 = EAS2(map)
alg4 = MINMAX(map)
algorithms = [alg1, alg2, alg3, alg4]
alg_names = ['ACO', 'ASRanked', 'EAS', 'MINMAX']
map_names = ['initMap', 'smallMap', 'mediumMap', 'largeMap']


# Set parameters here.
max_iterations = 10000
set_alpha = 10
set_beta = 10
set_pheromone = 1
optimal_percentage = 0
nr_tests = 10

# Returns the optimal path for a given map, food location, and current home location on this map. Hardcoded.
def getOptimalPath(map, food_pos, start_pos):
    optimalPath = 0
    if map.current_map == 0:
        optimalPath = 13
    elif map.current_map == 1:
        optimalPath = 14
    elif map.current_map == 2:
        # optimal for respectively (2, 13), (3, 8), (13, 2), and (13, 13)
        if food_pos == (2, 13) or food_pos == (3, 8):
            optimalPath = 15
        elif food_pos == (13, 2):
            optimalPath = 19
        elif food_pos == (13, 13):
            optimalPath = 24
    elif map.current_map == 3:
        # Optimal for respectively (3, 18), (14, 13), (18, 18)
        if food_pos == (3, 18) and start_pos == (1, 1):
            optimalPath = 19
        elif food_pos == (15, 12) and start_pos == (1, 1):
            optimalPath = 27
        elif food_pos == (18, 18) and start_pos == (1, 1):
            optimalPath = 34
        elif food_pos == (16, 3) and start_pos == (1, 1):
            optimalPath = 21
        elif food_pos == (3, 18) and start_pos == (4, 17):
            optimalPath = 2
        elif food_pos == (15, 12) and start_pos == (4, 17):
            optimalPath = 38
        elif food_pos == (18, 18) and start_pos == (4, 17):
            optimalPath = 39
        elif food_pos == (16, 3) and start_pos == (4, 17):
            optimalPath = 36
    return optimalPath

# Prepare csv file
with open('testResults.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    k = -1
    for alg in algorithms:
        k += 1
        writer.writerow(['Algorithm', 'Map', 'Alpha', 'Beta', 'Pheromone drop'])
        for i in range(map.nr_maps):
            avg_iterations = 0
            avg_percentage = 0
            writer.writerow([alg_names[k]] + [map_names[i]] + [str(set_alpha)] + [str(set_beta)] + [str(set_pheromone)])
            writer.writerow(['Test', 'Iterations', 'Percentage of rabbits with optimal path'])
            for j in range(nr_tests):
                rabbits = alg.getEntities()
                loop = True
                iterations = 0

                # Print details to console
                print('Algorithm: ' + alg_names[k])
                print('Test nr: ' + str(j))
                print('Map: ' + map_names[i])
                print('Start points: ' + str(map.getStartPos()))
                print('End points: ' + str(map.getEndPos()))
                print('Running...')

                while loop:
                    alg.update()
                    iterations += 1
                    optimalRabbits = 0
                    # When all rabbits have found an optimal path, stop looping
                    for rabbit in rabbits:
                        # Set parameter values
                        rabbit.alpha = set_alpha
                        rabbit.beta = set_beta
                        rabbit.pherodrop = set_pheromone
                        optimalPath = getOptimalPath(map, rabbit.found_food_pos, rabbit.initial_start_pos)
                        if rabbit.found_food == 1 and rabbit.best_path <= optimalPath:
                            optimalRabbits += 1
                    if optimalRabbits == len(rabbits):
                        loop = False
                    if iterations == max_iterations:
                        # prevent infinite looping
                        print('Max iterations reached')
                        loop = False
                    optimal_percentage = optimalRabbits / len(rabbits) * 100

                # Update statistics
                avg_iterations += iterations
                avg_percentage += optimal_percentage

                # Print results to console
                print('### RESULTS ###')
                print('Iterations: ' + str(iterations))
                print('Percentage of rabbits with optimal path: ' + str(optimal_percentage))
                print('found pathlength, optimal pathlength, startpoint, targetpoint, alpha, beta, Pheromone drop')
                for rabbit in rabbits:
                    print(' - ' + str(rabbit.color) + ': ' +
                          str(rabbit.best_path) + ', ' +
                          str(getOptimalPath(map, rabbit.found_food_pos, rabbit.initial_start_pos)) + ', ' +
                          str(rabbit.initial_start_pos) + ', ' +
                          str(rabbit.found_food_pos) + ', ' +
                          str(rabbit.alpha) + ', ' +
                          str(rabbit.beta) + ', ' +
                          str(rabbit.pherodrop))
                print('')

                # Write results to CSV file
                writer.writerow([str(j)] + [str(iterations)] + [str(optimal_percentage)])

            # Calculate and write average results
            avg_iterations /= nr_tests
            avg_percentage /= nr_tests
            writer.writerow(['Tests', 'Iterations avg', 'Percentage avg'])
            writer.writerow([str(nr_tests)] + [(str(avg_iterations))] + [str(avg_percentage)])

            if i < 4:
                # Go to next map
                map.setMap(i + 1)
                alg.__init__(map)
