import random
import numpy as np 
from code.algorithms.random_algo import random_algo
from code.algorithms.random_algo import get_randomize_solution
from code.classes.netlist import Netlist


""""Genetic algorithm"""
#from move_random.py import solution 

def start_population(netlist):
    start_population = []
    for i in range(10):
        start_population.append(get_randomize_solution(netlist))
    return start_population

def crossings(p1, p2):
    child = []
    pass

def best_population():
    pass

def random_pairs(population):
    pairs = []
    for i in range(len(population) // 2):
        pairs.append((population.pop(random.randrange(len(population))),
                        population.pop(random.randrange(len(population)))))
    for p in pairs:
        p1 = p[0]
        p2 = p[1]

    return pairs, p1, p2    
