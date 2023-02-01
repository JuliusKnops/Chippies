"""
(W.I.P.)
GeneticAlgorithm.py

Chippies
Julius Knops, Deniz Mermer, Hidde Brenninkmeijer
Algoritmen & Heuristieken

An attempt of a genetic heuristic combined with greedy 
to create new netlist solutions
(W.I.P.)
"""
import config
from code.algorithms.random_algo import get_randomize_solution
from code.classes.netlist import Netlist

from itertools import permutations
import math
import random
import copy
from typing import Tuple, TypeVar

MAX_INT = math.inf

MAX_X = 8
MAX_Y = 8
MAX_Z = 7

NetlistObject = TypeVar("NetlistObject")

# create start population by getting random solutions from randomise algorithm
def create_start_population(netlist: NetlistObject) -> list:
    """
    Create a starting population of size N by getting a random solution
    """
    start_population = []
    for Nsolution in range(config.PopulationSize):
        start_population.append(get_randomize_solution(netlist))
    return start_population

# create child by taking random paths from either of parents
def create_child(parent1: list, parent2: list) -> list:
    """
    Create new solution by taking random paths from parent1 or parent2
    """
    child = []
    for pathIndex in range(len(parent1)):
        if coin_toss() == 1:
            child.append(parent1[pathIndex])
        else:
            child.append(parent2[pathIndex])
    return child 

# return 50/50 chance value of 0 or 1
def coin_toss() -> int:
    """
    Returns 1 or 0, both with 50% chance
    """
    return random.randint(0, 1)

# create pairs of given population
def random_pairs(StartPopulation: list) -> list:
    """
    Create a list where two random solutions from population 
    are paired as parent1 and parent2
    """
    pairs = []
    population = copy.deepcopy(StartPopulation)
    number_of_pairs = len(population) // 2
    for Npair in range(number_of_pairs):
        pairs.append((population.pop(random.randrange(len(population))),
                        population.pop(random.randrange(len(population)))))
    return pairs  


def genetic(pairs: list, populatie: list) -> list:
    """
    For each pair of parents, create child solutions.
    Check if paths of new solution are mutated
    Mutated paths are remade with a greedy algorithm
    """
    # for each pair
    for Npair in pairs:
        # create child solution
        child = create_child(Npair[0], Npair[1])
        # mutate child
        child, path = mutate(child)
        # take best solution of mutation
        best_child = create_mutated_child(child, path)

        # check if child solution has valid paths
        if check_valid_mutation(best_child):
            populatie.append(best_child)

    return populatie

def check_valid_mutation(child: list) -> bool:
    invalidchild = False
    for path in child:
        if path is None:
            return False
    
    if len(child) != 0:
        return True
    

def mutate(child: list) -> list:
    """
    There is chance (P) to mutate each path of child.
    """
    new_path = set()
    for path in child:
        if path is None:
            continue
        if config.MutateChance >= random.uniform(0, 1):
            start = path[0]
            end = path[-1]
            new_path.add((child.index(path), start, end))
            child[child.index(path)] = None
    
    return child, new_path

def create_mutated_child(child: list, new_path: set) -> list:
    """
    Create paths with greedy that are assigned as mutated paths
    """
    location_paths = new_path
    score_child = MAX_INT
    permutations_paths = list(permutations(new_path))
    best_child = []


    # for each possible permutations for child
    for mutated_paths in permutations_paths:
       
        visited = set()
        add_paths_child = []
        new_child = True
        # create visited nodes
        for paths in child:
            if paths is None:
                continue
            for nodes in paths:
                visited.add(nodes)

        # for all new paths in mutated_paths
        for path in mutated_paths:
            new_child = True

            # create new path with greedy
            new_path = greedy(path, visited)
            
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
            for x in location_paths:
                for p in add_paths_child:
                    if p[0] == x[1] and p[-1] == x[2]:
                        child[x[0]] = p

        
            current_child_score = calculate_cost(child)
            if current_child_score <= score_child:
                score_child = current_child_score
                best_child = child
        
    return best_child
   

def greedy(points: tuple, visited: set) -> list:
    """
    Create with greedy a connection between two points
    The new path cannot go over previously visited nodes.
    """
    start_point = points[1]
    end_point = points[2]
    possible_moves = [(1,0,0), (0,1,0), (0,0,1), (-1,0,0), (0,-1,0), (0,0,-1)]
    path_found = False
    path = []
    new_pos = start_point
    while not path_found:
        prev_best_distance = MAX_INT
        for moves in possible_moves:
            new_pos = calculate_wire_pos(new_pos, moves, '+')
            current_distance = calculate_euclidean(new_pos, end_point)
            
            if valid_node(new_pos, visited, path) and \
               current_distance < prev_best_distance:

                prev_best_distance = current_distance
                next_move = moves 
            new_pos = calculate_wire_pos(new_pos, moves, '-')
            
        if prev_best_distance == MAX_INT:
            return []

        path.append(new_pos)
        new_pos = calculate_wire_pos(new_pos, next_move, '+')

        path, path_found = check_goal(new_pos, path, end_point)
    return path

def count_crossings(child: list) -> int:
    """
    Count the number of crossings being made in given solution
    """
    crossing = []
    for path in child:
        if path is None:
            continue
        path = path[1:len(path) - 1]
        for node in path:
            crossing.append(node)
    
    return len(crossing) - len(set(crossing))

def is_valid(child: list) -> bool:
    """
    Check if there are no overlapping of wires in given solution
    """
    valid = []
    for path in child:
        for node in range(len(path) - 1):
            valid.append((path[node], path[node + 1]))

    return len(valid) == len(set(valid))    

def calculate_cost(child: list) -> int:
    """
    Calculates cost of given solution by counting the number of 
    units used (total length of wires) and the amount of crossings
    present in given solution
    """
    return count_units(child) + 300 * count_crossings(child)

def count_units(child: list) -> int:
    """
    Count the total number of units used (total length of wires)
    """
    units = 0
    for path in child:
        if path is None:
            continue
        units += len(path) - 1
    return units

def out_of_bounds(current_node: tuple) -> bool:
    """
    Check if new move to new node does not go out of bounds
    """
    return not (0 <= current_node[0] <= MAX_X and 
                0 <= current_node[1] <= MAX_Y and 
                0 <= current_node[2] <= MAX_Z)

def valid_node(current_node: tuple, visited: set, path: list) -> bool:
    """
    Check if new move to new node is valid, not previously visited 
    and not out of bounds
    """
    return (not (current_node in visited or current_node in path)) and \
            not out_of_bounds(current_node)
    
def calculate_wire_pos(new_wire_location: tuple, 
                       random_move: tuple, dir: str) -> tuple:
    """
    Return new position of wire after a new move
    """
    if dir == '+':
        return (new_wire_location[0] + random_move[0], 
                new_wire_location[1] + random_move[1], 
                new_wire_location[2] + random_move[2])
    return (new_wire_location[0] - random_move[0], 
            new_wire_location[1] - random_move[1], 
            new_wire_location[2] - random_move[2])

def check_goal(new_wire_location: tuple, path: list, 
               end_gate: tuple, visited: set) -> Tuple[list, bool]:
    """
    When wire is 1 valid move removed from end gate, make that connection
    """
    dx = new_wire_location[0] - end_gate[0]
    dy = new_wire_location[1] - end_gate[1]
    dz = new_wire_location[2] - end_gate[2]

    if (dx, dy, dz) in [(1,0,0), (0,1,0), (0,0,1), 
                        (-1,0,0), (0,-1,0), (0,0,-1)]:
        
        path.append(end_gate)
        found_path = True 
        return path, found_path

    return path, False

def calculate_euclidean(pos1: tuple, pos2: tuple) -> float:
    """
    Calculate the eaclidean distance between two given points
    """
    euclidean_distance = math.sqrt((pos1[0] - pos2[0])**2 + 
                                    (pos1[1] - pos2[1])**2 + 
                                    (pos1[2] - pos2[2])**2)
    return euclidean_distance

def start_genetic(netlist: NetlistObject) -> list:
    startpopulation = create_start_population(netlist)
    for iteration in range(config.NumberOfGenerations):
        pairs = random_pairs(startpopulation)

        startpopulation = genetic(pairs, startpopulation)

        population_scores = []
        for sol in startpopulation:
            score_sol = calculate_cost(sol)
            population_scores.append([score_sol, sol])
            
        

        population_scores = sorted(population_scores, key=lambda x: x[0])
        population_scores = population_scores[:config.PopulationSize]
        
        population = []
        for x in startpopulation:
            sol = x[1]
            
            population.append(sol)

        
        startpopulation = population


    print(f"startpopulatie = {len(startpopulation)}")
    print(population_scores[0])
    return startpopulation
