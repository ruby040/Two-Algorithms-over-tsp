import math
import random
import time  
# ------------------------
#   Reading the TSP file
# -------------------------

def read_tsp_file(filename):
    cities = []
    reading = False 

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line == 'NODE_COORD_SECTION':
                reading = True 
                continue
            if line == 'EOF':
                break 

            if reading:
                parts = line.split()
                # split the line into x and y coordinates for the city
                x = float(parts[1])
                y = float(parts[2])
                cities.append((x, y))
    return cities


# ------------------------
#  Path and distance calculations
# ------------------------

def euclidean_distance(city1, city2):
    # calculate the straight-line distance between two cities using the distance formula
    return math.sqrt((city1[0] - city2[0])**2 + (city1[1] - city2[1])**2)


def total_distance(tour, cities):
    # sum all path distances and return to the starting point
    dist = 0
    n = len(tour)
    for i in range(n):
        city_a = cities[tour[i]]
        city_b = cities[tour[(i + 1) % n]] 
        dist += euclidean_distance(city_a, city_b)
    return dist


# -----------------------
#  Movement operations
# ---------------------

def random_tour(n):
    # create a random tour as the starting point for each firefly
    tour = list(range(n))
    random.shuffle(tour)
    return tour


def swap_move(tour):
    # random swap move needed for exploration
    new_tour = tour[:] 
    i, j = random.sample(range(len(tour)), 2) 
    new_tour[i], new_tour[j] = new_tour[j], new_tour[i] 
    return new_tour


# ---------------------------------
#   Firefly Algorithm (core)
# ---------------------------------

def firefly_algorithm(cities, num_fireflies=20, num_iterations=500, alpha=0.5, seed=None):
    
    # the seed fixes the randomness
    # set so that running the code multiple times always produces the same results
    # like a password that keeps the random process on the same path every time
    if seed is not None:
        random.seed(seed)

    n = len(cities)

    # initialize the fireflies, each with a random tour
    fireflies = [random_tour(n) for _ in range(num_fireflies)]
    
    # calculate brightness: shorter distance means higher brightness
    brightness = [-total_distance(f, cities) for f in fireflies]

    # track the best tour found so far
    best_idx = brightness.index(max(brightness))
    best_tour = fireflies[best_idx][:]
    best_distance = -brightness[best_idx]

    # main loop of the firefly algorithm
    for iteration in range(num_iterations):
        for i in range(num_fireflies):
            for j in range(num_fireflies):
                
                # firefly i is attracted to firefly j
                # if j's tour is better than i's tour
                if brightness[j] > brightness[i]:
                    
                    if random.random() < alpha:
                        # create a new tour using a random swap move (exploration)
                        new_tour = swap_move(fireflies[i])
                    else:
                        # create a new tour by taking a segment from the better tour (exploitation)
                        new_tour = fireflies[i][:]
                        start = random.randint(0, (n - 2))
                        end = random.randint((start + 1), (n - 1))
                        segment = fireflies[j][start:end]
                        rest = [c for c in fireflies[i] if c not in segment]
                        new_tour = (rest[:start] + segment + rest[start:])

                    # check if the new tour is better than the current one
                    new_brightness = -total_distance(new_tour, cities)
                    if new_brightness > brightness[i]:
                        fireflies[i] = new_tour
                        brightness[i] = new_brightness

        # update the global best tour
        current_best_idx = brightness.index(max(brightness))
        if -brightness[current_best_idx] < best_distance:
            best_tour = fireflies[current_best_idx][:]
            best_distance = -brightness[current_best_idx]

    return best_tour, best_distance


# -----------------------------
#    Running and measuring runtime
# ------------------------------

if __name__ == "__main__":
 
    # the datasets to run on
    instances = [
        ("data/eil51.tsp", "eil51"),
        ("data/pr264.tsp", "pr264")
    ]
 
    # run on each dataset
    for filename, name in instances:
        cities = read_tsp_file(filename)
        print(f"\n{'='*50}")
        print(f"Running Firefly Algorithm on {name} ({len(cities)} cities)")
        print(f"{'='*50}")
 
        # run 20 different runs with a different seed each time
        for seed in range(1, 21):
            start_time = time.time()
 
            best_tour, best_dist = firefly_algorithm(
                cities,
                num_fireflies=20,
                num_iterations=1000,
                alpha=0.5,
                seed=seed  # each run uses a different seed so results are independent
            )
 
            end_time = time.time()
            runtime = end_time - start_time
 
            # print results for each run
            print(f"Run {seed:02d} | Best Distance: {best_dist:.2f} | Runtime: {runtime:.4f}s")