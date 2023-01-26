import random
import numpy as np 
from code.algorithms.random_algo import random_algo
from code.algorithms.random_algo import get_randomize_solution
from code.classes.netlist import Netlist

from itertools import permutations
import math

import copy

""""Genetic algorithm"""
#from move_random.py import solution 

def start_population(netlist):
    start_population = []
    for i in range(10):
        start_population.append(get_randomize_solution(netlist))
    return start_population

def crossings(p1, p2):
    child = []
    for i in range(len(p1)):
        if coin_toss() == 1:
            child.append(p1[i])
        else:
            child.append(p2[i])
    return child 

def coin_toss():
    return random.randint(0, 1)

def p(pairs, populatie):
    #print(f"PAIRS = {pairs}")
    for i in pairs:
        # pairs = [(p1, p2), ()]
        # i = (p1, p2)
        #print(f"PARENT 1 = {i[0]}")
        #print(f"PARENT 2 = {i[1]}")
        child = crossings(i[0], i[1])
        child, path = mutate(child)
        best_child = create_path(child, path)
        # voeg toe aan verzameling / populatie
        print("ADD CHILD")
        populatie.append(best_child)
        print(f"grootte populatie = {len(populatie)}")
    return populatie

def random_pairs(populationX):
    pairs = []
    population = copy.deepcopy(populationX)
    for i in range(len(population) // 2):
        pairs.append((population.pop(random.randrange(len(population))),
                        population.pop(random.randrange(len(population)))))
    return pairs  


def mutate(child):
    new_path = set()
    P = 0.5
    for path in child:
        if P >= random.uniform(0, 1):
            start = path[0]
            end = path[-1]
            new_path.add((child.index(path), start, end))
            child[child.index(path)] = None
    
    # check if valid child

    return child, new_path

def create_path(child, new_path):
    location_paths = new_path
    score_child = 9999999999
    permutations_paths = list(permutations(new_path))
    for order in permutations_paths:
       
        visited = set()
        add_paths_child = []
        
        for x in child:
            if x is None:
                continue
            for p in x:
                
                visited.add(p)

        for x in order:
            # Create new paths with greedy
            new_child = True
            new_path = greedy2(x, visited)
            #print(f"NEW PATH = {new_path}")
            
            if new_path == []:
                new_child = False
                break

            # update visited nodes
            for x in new_path:
                visited.add(x)
        
            add_paths_child.append(new_path)
            
        

        if len(add_paths_child) == 0:
            new_child = True

        if new_child:
            #print(f"location paths = {location_paths}")
            for x in location_paths:
                
                for p in add_paths_child:
                    #print(f"p = {p}")
                    if p[0] == x[1] and p[-1] == x[2]:
                        child[x[0]] = p 
        
            #print(child)
        
            current_child_score = calculate_cost(child)
            if current_child_score < score_child:
                score_child = current_child_score
                best_child = child
        
        # calc doelfuntie score -> opslaan als beste
    # beste returnen.
    # print(best_child)
    # print(calculate_cost(best_child))
    return best_child


def count_crossings(child):
        crossing = []
        for path in child:
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
        units += len(path) - 1
    return units


# functies aanpassen naar class functies -> class variables aanmaken voor visited en path, zodat aantal parameters naar netlist en location gaan.
def out_of_bounds(current_node):
    return not (0 <= current_node[0] <= 8 and 0 <= current_node[1] <= 8 and 0 <= current_node[2] <= 7)
# functies aanpassen naar class functies -> class variables aanmaken voor visited en path, zodat aantal parameters naar netlist en location gaan.
def valid_node(current_node, visited, path):
    return (not (current_node in visited or current_node in path)) and not out_of_bounds(current_node)

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
    print(len(startpopulation))
    pairs = random_pairs(startpopulation)

    startpopulation = p(pairs, startpopulation)

    print(f"startpopulatie = {len(startpopulation)}")

    # [score, [[(), ()], [(), ()]]]

    startpopulation = startpopulation[:10]
    print(f"startpopulatie = {len(startpopulation)}")
    return #startpopulation


# if __name__ == "__main__":
#     chip_nr = 0 # loopt van 0 tot en met 2
#     netlist_nr = 1 # loopt van 1 tot en met 3

#     netlist_file = f"data/chip_{chip_nr}/netlist_{netlist_nr + 3 * chip_nr}.csv"
#     print_file = f"data/chip_{chip_nr}/print_{chip_nr}.csv"
    
#     netlist = Netlist.Netlist(netlist_file, print_file)

#     startpopulation = start_population(netlist)
#     pairs = random_pairs(startpopulation)

#     startpopulation = p(pairs, startpopulation)

#     print(f"startpopulatie = {startpopulation}")
#     startpopulation = startpopulation[:10]
#     print(f"startpopulatie = {startpopulation}")

