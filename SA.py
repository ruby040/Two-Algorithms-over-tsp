import math
import numpy as np
import random

CitiesOf_eil51 = [
    (37, 52),(49, 49),(52, 64),(20, 26),(40, 30),
    (21, 47),(17, 63),(31, 62),(52, 33),(51, 21),
    (42, 41),(31, 32),(5, 25),(12, 42),(36, 16),(52, 41),
    (27, 23),(17, 33),(13, 13),(57, 58),(62, 42),
    (42, 57),(16, 57),(8, 52),(7, 38),(27, 68),
    (30, 48),(43, 67),(58, 48),(58, 27),(37, 69),
    (38, 46),(46, 10),(61, 33),(62, 63),(63, 69),
    (32, 22),(45, 35),(59, 15),(5, 6),(10, 17),
    (21, 10),(5, 64),(30, 15),(39, 10),(32, 39),(25, 32),(25, 55),
    (48, 28),(56, 37),(30, 40)
]

CitiesOf_Pr264 = [
    (3425, 6450),(3625, 3200),(3525, 3200),(3525, 3350),(3625, 3350),(3725, 3350),(3725, 3650),(3625, 3650),(3525, 3650),(3525, 3850),(3625, 3850),(3725, 3850),(3725, 4150),(3625, 4150),(3525, 4150),(3525, 4350),(3625, 4350),(3725, 4350),(3725, 4650),(3625, 4650),(3525, 4650),(3525, 4850),(3625, 4850),(3725, 4850),(3725, 5150),(3625, 5150),(3525, 5150),(3525, 5350),(3625, 5350),(3725, 5350),(3725, 5650),(3625, 5650),(3525, 5650),(3525, 5850),(3625, 5850),(3725, 5850),(3725, 6150),(3625, 6150),(3525, 6150),(3525, 6450),(3525, 6650),(3675, 7150),(3675, 7500),(3675, 7700),(3675, 7850),(3675, 8050),(3525, 8300),(3625, 8300),(3725, 8300),(3725, 8600),(3625, 8600),(3525, 8600),(3825, 8750),(3925, 8750),(3925, 8600),(3825, 8600),(3825, 8300),(3925, 8300),(3925, 7600),(3925, 6150),(3825, 6150),(3825, 5850),(3925, 5850),(3925, 5650),(3825, 5650),(3825, 5350),(3925, 5350),(3925, 5150),(3825, 5150),(3825, 4850),(3925, 4850),(3925, 4650),(3825, 4650),(3825, 4350),(3925, 4350),(3925, 4150),(3825, 4150),(3825, 3850),(3925, 3850),(3925, 3650),(3825, 3650),(3825, 3350),(3925, 3350),(3875, 3200),(4075, 3200),
]

def Create_Distance_Matrix(Cities):

    Number_Of_Cities = len(Cities)

    matrix = np.zeros((Number_Of_Cities, Number_Of_Cities))

    for i in range(Number_Of_Cities):

        for j in range(Number_Of_Cities):

            if i != j:

                x1, y1 = Cities[i]
                x2, y2 = Cities[j]

                d = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

                matrix[i][j] = d

    return matrix
    
Matrix_eil51 = Create_Distance_Matrix(CitiesOf_eil51)
Matrix_Pr264 =Create_Distance_Matrix(CitiesOf_Pr264)


def Create_Starting_Path(Number_Of_Cities):

    path = list(range(Number_Of_Cities))
    random.shuffle(path)
    return path
    
def Create_Neighbor_Path(current_path):
    neighbor_path = current_path.copy()
    number_of_cities = len(current_path)
    random_index = random.randint(1, number_of_cities - 1)
    reverse_part = []

    for i in range(random_index, random_index + 6):
        if i < number_of_cities:
            reverse_part.append(current_path[i])
    reverse_part = reverse_part[::-1]
    reverse_counter = 0
    
    for i in range(random_index, random_index + len(reverse_part)):
        neighbor_path[i] = reverse_part[reverse_counter]
        reverse_counter += 1
        
    return neighbor_path
    
def Calculate_Path_Cost(path, matrix):
    total_cost = 0
    number_of_cities = len(path)
    
    for i in range(number_of_cities - 1):
        city1 = path[i]
        city2 = path[i + 1]
        total_cost += matrix[city1][city2]

    total_cost += matrix[path[-1]][path[0]]
    return total_cost
    
temperature = 100
#alpha =  0.90#float(input("Enter Alpha: "))
#max_iterations = 25 #int(input("Enter Maximum Iterations: "))
    

starting_path = Create_Starting_Path(len(CitiesOf_eil51)) 
Best_path_found = starting_path
#Cost_BPF = Calculate_Path_Cost(Best_path_found)
Current_path = starting_path

    
def Simulated_Annealing(matrix, alpha, max_iterations):

    temperature = 100

    starting_path = Create_Starting_Path(len(matrix))

    Best_path_found = starting_path.copy()
    Current_path = starting_path.copy()

    while max_iterations != 0 and temperature > 0.1:

        Neighbor_path = Create_Neighbor_Path(Current_path)

        Delta_E = Calculate_Path_Cost(Current_path, matrix) - Calculate_Path_Cost(Neighbor_path, matrix)

        if Delta_E > 0:
            Current_path = Neighbor_path.copy()

        else:
            probability = math.exp(Delta_E / temperature)

            if random.random() < probability:
                Current_path = Neighbor_path.copy()

        if Calculate_Path_Cost(Current_path, matrix) < Calculate_Path_Cost(Best_path_found, matrix):
            Best_path_found = Current_path.copy()

        temperature = alpha * temperature
        max_iterations -= 1

    Cost_BPF = Calculate_Path_Cost(Best_path_found, matrix)

    print("Best Path Found:")
    print(Best_path_found)

    print("Best Path Cost:")
    print(Cost_BPF)
    
    
#------------------------------------------------------
alpha = 0.99
max_iterations = 10000

print("--------- eil51 ---------")

Simulated_Annealing( Matrix_eil51, alpha, max_iterations )

print("\n--------- Pr264 ---------")

Simulated_Annealing( Matrix_Pr264, alpha, max_iterations )

    
