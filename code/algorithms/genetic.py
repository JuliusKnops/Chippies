import random
import numpy as np 
from code.algorithms.random_algo import random_algo
from code.algorithms.random_algo import get_randomize_solution
from code.classes.netlist import Netlist

from itertools import permutations
import math

import copy
from queue import PriorityQueue

""""Genetic algorithm"""
#from move_random.py import solution 

# create start population by getting random solutions from randomise algorithm
def start_population(netlist):
    start_population = []
    for i in range(50):
        start_population.append(get_randomize_solution(netlist))
    return start_population

# create child by taking random paths from either of parents
def create_child(p1, p2):
    child = []
    #print(f"P1 = {p1} | P2 = {p2}")
    for i in range(len(p1)):
        if coin_toss() == 1:
            child.append(p1[i])
        else:
            child.append(p2[i])
    return child 

# return 50/50 chance value
def coin_toss():
    return random.randint(0, 1)

# create pairs of given population
def random_pairs(populationX):
    pairs = []
    population = copy.deepcopy(populationX)
    for i in range(len(population) // 2):
        pairs.append((population.pop(random.randrange(len(population))),
                        population.pop(random.randrange(len(population)))))
    return pairs  

# 
def genetic(pairs, populatie):
    # for each pair
    for i in pairs:
        # create child solution
        child = create_child(i[0], i[1])
        # mutate child
        child, path = mutate(child)
        best_child = fix_child(child, path)

        invalidchild = False
        for x in best_child:
            if x is None:
                invalidchild = True 
                break
        
        if invalidchild:
            continue
        
        if len(best_child) != 0:
            populatie.append(best_child)
    return populatie

# get paths that need to be mutated
def mutate(child):
    new_path = set()
    P = 0.5
    for path in child:
        if path is None:
            continue
        if P >= random.uniform(0, 1):
            start = path[0]
            end = path[-1]
            new_path.add((child.index(path), start, end))
            child[child.index(path)] = None
    
    return child, new_path

def fix_child(child, new_path):
    location_paths = new_path
    score_child = 9999999999
    permutations_paths = list(permutations(new_path))
    best_child = []


    # for each possible permutations for child
    for order in permutations_paths:
       
        visited = set()
        add_paths_child = []
        new_child = True
        # create visited nodes
        for paths in child:
            if paths is None:
                continue
            for nodes in paths:
                visited.add(nodes)

        # for all new paths in order
        for x in order:
            new_child = True

            # create new path with greedy
            start = x[1]
            end = x[2]
            #print(f"start = {start} | end = {end}")
            #new_path = find_path(start, end, visited)
            new_path = greedy2(x, visited)
            
            # if empty list is returned, no valid path can be made with greedy
            if new_path == []:
                new_child = False
                break

            # update visited nodes
            for x in new_path:
                visited.add(x)
        
            add_paths_child.append(new_path)
            
            
        if len(add_paths_child) == 0 and new_child:
            new_child = True

        if new_child:
            #print(f"location paths = {location_paths}")
            for x in location_paths:
                #print(f"x = {x}")
                for p in add_paths_child:
                    #print(f"p = {p}")
                    if p[0] == x[1] and p[-1] == x[2]:
                        #print(f"{child[x[0]]} = {p}")
                        child[x[0]] = p

            for i in child:
                if i is None:
                    print("NONE PATH FOUND")
                    
            #print(child)
        
            current_child_score = calculate_cost(child)
            if current_child_score <= score_child:
                score_child = current_child_score
                best_child = child
        
        # calc doelfuntie score -> opslaan als beste
    # beste returnen.
    # print(best_child)
    # print(calculate_cost(best_child))
    # if best_child:
    return best_child
   
###
def greedy2(points, visited):
    start_point = points[1]
    end_point = points[2]
    possible_moves = [(1,0,0), (0,1,0), (0,0,1), (-1,0,0), (0,-1,0), (0,0,-1)]
    path_found = False
    path = []
    new_pos = start_point
    while not path_found:
        prev_best_distance = 999999999
        for moves in possible_moves:
            #print(f"moves = {moves}")
            new_pos = calculate_wire_pos(new_pos, moves, '+')
            #print(f"new pos = {new_pos}") 
            current_distance = calculate_euclidean(new_pos, end_point)
            
            if valid_node(new_pos, visited, path) and current_distance < prev_best_distance:
                #print("NEW MOVE VALID")
                prev_best_distance = current_distance
                next_move = moves 
            new_pos = calculate_wire_pos(new_pos, moves, '-')
            
        

        if prev_best_distance == 999999999:
            return []

        path.append(new_pos)
        #print(f"next_move = {next_move} | path = {path}")
        new_pos = calculate_wire_pos(new_pos, next_move, '+')

        path, path_found = check_goal(new_pos, path, end_point)
    return path

def find_path(start, end, visited):
    # Create a 3D list to keep track of visited cells
    n = 7
    m = 7
    l = 7
    #visited = [[[False for _ in range(n+1)] for _ in range(m+1)] for _ in range(l+1)]
    # Create a priority queue to store next cells to visit
    q = PriorityQueue()
    # Create a dictionary to keep track of the previous cell visited for each cell
    prev = {}
    # Add the starting node to the priority queue with a priority of 0
    q.put((0, start))
    # Mark the starting node as visited
    visited.add((start[0],start[1],start[2]))
    # Set the distance from the start node to 0
    dist = 0

    while not q.empty():
        # Get the next cell to visit
        curr_dist, curr_cell = q.get()
        # Check if the current cell is the end node
        if curr_cell == end:
            # Trace back the path from the end node to the start node
            path = []
            while curr_cell in prev:
                path.append(curr_cell)
                curr_cell = prev[curr_cell]
            # Return the reversed path list
            path.append(start)
            return path[::-1]
        # Iterate through each direction (x, y, z)
        for dx, dy, dz in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]:
            # Calculate the new cell location
            new_x, new_y, new_z = curr_cell[0] + dx, curr_cell[1] + dy, curr_cell[2] + dz
            # Check if the new cell is not out of the grid and not an obstacle
            if 0 <= new_x <= n and 0 <= new_y <= m and 0 <= new_z <= l and (new_x, new_y, new_z) not in visited:
                # if not visited[new_x][new_y][new_z]:
                # Set the previous cell for the new cell as the current cell
                prev[(new_x, new_y, new_z)] = curr_cell
                # Mark the new cell as visited
                visited.add((new_x, new_y, new_z)) #visited[new_x][new_y][new_z] = True
                # Add the new cell to the priority queue with a priority of curr_dist + 1
                q.put((curr_dist + 1, (new_x, new_y, new_z)))

    # Return "Path not found" if the end node has not been reached
    return []

def count_crossings(child):
        crossing = []
        for path in child:
            if path is None:
                continue
            path = path[1:len(path) - 1]
            for node in path:
                crossing.append(node)
        
        return len(crossing) - len(set(crossing))

def is_valid(child):
    valid = []
    for path in child:
        for node in range(len(path) - 1):
            valid.append((path[node], path[node + 1]))

    return len(valid) == len(set(valid))    

def calculate_cost(child):
    return count_units(child) + 300 * count_crossings(child)

def count_units(child):
    units = 0
    for path in child:
        if path is None:
            continue
        units += len(path) - 1
    return units

# functies aanpassen naar class functies -> class variables aanmaken voor visited en path, zodat aantal parameters naar netlist en location gaan.
def out_of_bounds(current_node):
    return not (0 <= current_node[0] <= 8 and 0 <= current_node[1] <= 8 and 0 <= current_node[2] <= 7)
# functies aanpassen naar class functies -> class variables aanmaken voor visited en path, zodat aantal parameters naar netlist en location gaan.
def valid_node(current_node, visited, path):
    return (not (current_node in visited or current_node in path)) and not out_of_bounds(current_node)
    
def calculate_wire_pos(new_wire_location, random_move, dir):
    if dir == '+':
        return (new_wire_location[0] + random_move[0], new_wire_location[1] + random_move[1], new_wire_location[2] + random_move[2])
    return (new_wire_location[0] - random_move[0], new_wire_location[1] - random_move[1], new_wire_location[2] - random_move[2])

def check_goal(new_wire_location, path, end_gate):
    if (new_wire_location[0] - end_gate[0], new_wire_location[1] - end_gate[1], new_wire_location[2] - end_gate[2]) in [(1,0,0), (0,1,0), (-1,0,0), (0,-1,0), (0,0,1), (0,0,-1)]:
        path.append(new_wire_location)
        path.append(end_gate)
        found_path = True 
        return path, found_path
    return path, False

def calculate_euclidean(pos1, pos2):
    euclidean_distance = math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2 + (pos1[2] - pos2[2])**2)
    return euclidean_distance


def create_new_pop(netlist):
    startpopulation = start_population(netlist)
    # print(len(startpopulation))
    # for i in range(50):
    #     print(len(startpopulation))
    for i in range(100):
        pairs = random_pairs(startpopulation)

        startpopulation = genetic(pairs, startpopulation)

        # print(f"startpopulatie = {len(startpopulation)}")

        # [score, [[(), ()], [(), ()]]]

        startpopulation2 = []
        for sol in startpopulation:
            score_sol = calculate_cost(sol)
            startpopulation2.append([score_sol, sol])
            
        #print(startpopulation2)

        startpopulation2 = sorted(startpopulation2, key=lambda x: x[0])
        pop_with_val = startpopulation2
        #print(startpopulation2)

        startpopulation = startpopulation2[:50]
        #startpopulation = [sol for sol[1] in startpopulation]
        
        startpopulation2 = []
        for x in startpopulation:
            sol = x[1]
            #print(f"SOLUTION = {sol}")
            startpopulation2.append(sol)


        # print("########################################")
        # print(startpopulation)
        
        startpopulation = startpopulation2


        ###
        # beginpopulatie = [[oplossing1], [oplossing2], etc]
        # nieuwe populatie = [[score1, [oplossing1]], [score2, [oplossing2]], etc]
        ###

    print(f"startpopulatie = {len(startpopulation)}")
    print(pop_with_val[0])
    return #startpopulation
