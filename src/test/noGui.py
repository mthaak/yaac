from src.alg.ACO import ACO
from src.map.Map import Map

map = Map()
alg = ACO(map)

map.__init__()
alg.__init__(map)

# Set parameters here.
max_iterations = 100000
set_alpha = 10
set_beta = 10
set_pheromone = 1
optimal_percentage = 0

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

for i in range(map.nr_maps):
    rabbits = alg.getEntities()
    loop = True
    iterations = 0

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
            optimalPath = getOptimalPath(map, rabbit.found_food_pos, rabbit.current_start_pos)
            if rabbit.found_food == 1 and rabbit.best_path <= optimalPath:
                optimalRabbits += 1
        if optimalRabbits == len(rabbits):
            loop = False
        if iterations == max_iterations:
            # prevent infinite looping
            print('Max iterations reached.')
            loop = False
        optimal_percentage = optimalRabbits / len(rabbits) * 100

    # Print results.
    print('Map: ' + str(map.current_map) + ' (0 = initMap, 1 = smallMap, 2 = mediumMap, 3 = largeMap)')
    print('Startingpoints: ' + str(map.getStartPos()) + ', Food places: ' + str(map.getEndPos()))
    print('Iterations: ' + str(iterations) + 'Optimal percentage: ' + optimal_percentage)
    print('found pathlength, optimal pathlength, startpoint, targetpoint, alpha, beta, Pheromone drop')
    for rabbit in rabbits:
        print(' - ' + str(rabbit.color) + ': ' +
              str(rabbit.best_path) + ', ' +
              str(getOptimalPath(map, rabbit.found_food_pos, rabbit.current_start_pos)) + ', ' +
              str(rabbit.current_start_pos) + ', ' +
              str(rabbit.found_food_pos) + ', ' +
              str(rabbit.alpha) + ', ' +
              str(rabbit.beta) + ', ' +
              str(rabbit.pherodrop))
    # Go to next map
    map.toggleMap()
    alg.__init__(map)