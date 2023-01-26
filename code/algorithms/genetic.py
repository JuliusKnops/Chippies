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
    for i in range(len(p1)):
        if coin_toss() == 1:
            child.append(p1[i])
        else:
            child.append(p2[i])
    return child 

def coin_toss():
    return random.randint(0, 1)


def random_pairs(population):
    pairs = []
    for i in range(len(population) // 2):
        pairs.append((population.pop(random.randrange(len(population))),
                        population.pop(random.randrange(len(population)))))
    return pairs  


