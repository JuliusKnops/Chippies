import random
import numpy as np 

""""Genetic algorithm"""
#from move_random.py import solution 

parent1 = [[(1, 5, 0), (2, 5, 0), (2, 4, 0), (2, 3, 0), (1, 3, 0), (0, 3, 0), (0, 2, 0), (0, 1, 0), (0, 1, 1), (0, 2, 1), (0, 3, 1), (0, 3, 2), (0, 4, 2), (0, 5, 2), (0, 6, 2), (1, 6, 2), (1, 6, 3), (2, 6, 3), (2, 6, 2), (2, 7, 2), (3, 7, 2), (3, 7, 1), (4, 7, 1), (5, 7, 1), (5, 7, 0), (6, 7, 0), (6, 6, 0), (6, 6, 0), (6, 5, 0)], [(1, 5, 0), (1, 6, 0), (1, 7, 0), (2, 7, 0), (3, 7, 0), (4, 7, 0), (4, 6, 0), (4, 5, 0), (4, 5, 0), (4, 4, 0)], [(4, 4, 0), (3, 4, 0), (3, 3, 0), (3, 2, 0), (3, 2, 0), (3, 1, 0)], [(6, 2, 0), (5, 2, 0), (5, 2, 1), (5, 3, 1), (5, 4, 1), (5, 4, 0), (5, 3, 0), (6, 3, 0), (7, 3, 0), (7, 4, 0), (6, 4, 0), (6, 4, 0), (6, 5, 0)], [(6, 2, 0), (6, 1, 0), (6, 0, 0), (7, 0, 0), (7, 0, 1), (6, 0, 1), (6, 1, 1), (6, 1, 2), (7, 1, 2), (7, 1, 3), (7, 1, 4), (7, 0, 4), (6, 0, 4), (6, 0, 3), (7, 0, 3), (7, 0, 2), (6, 0, 2), (5, 0, 2), (5, 1, 2), (5, 1, 3), (5, 0, 3), (4, 0, 3), (3, 0, 3), (2, 0, 3), (2, 1, 3), (3, 1, 3), (3, 2, 3), (2, 2, 3), (2, 2, 2), (2, 1, 2), (2, 0, 2), (3, 0, 2), (3, 0, 1), (3, 0, 0), (3, 0, 0), (3, 1, 0)]]

child =  [[(1, 5, 0), (1, 6, 0), (0, 6, 0), (0, 7, 0), (0, 7, 1), (0, 7, 2), (0, 6, 2), (1, 6, 2), (1, 7, 2), (2, 7, 2), (2, 7, 1), (2, 6, 1), (3, 6, 1), (3, 7, 1), (4, 7, 1), (4, 6, 1), (4, 6, 0), (5, 6, 0), (5, 7, 0), (5, 7, 1), (6, 7, 1), (6, 7, 2), (7, 7, 2), (7, 7, 1), (7, 6, 1), (7, 5, 1), (6, 5, 1), (6, 6, 1), (5, 6, 1), (5, 6, 2), (5, 6, 3), (4, 6, 3), (3, 6, 3), (3, 5, 3), (3, 5, 4), (3, 4, 4), (3, 4, 3), (3, 3, 3), (4, 3, 3), (4, 4, 3), (4, 4, 2), (4, 4, 1), (4, 4, 0)], [(1, 5, 0), (0, 5, 0), (0, 5, 1), (0, 5, 2), (0, 4, 2), (0, 4, 1), (0, 4, 0), (0, 3, 0), (1, 3, 0), (1, 3, 1), (2, 3, 1), (2, 3, 2), (2, 3, 3), (2, 3, 4), (2, 3, 5), (2, 3, 6), (2, 3, 7), (2, 2, 7), (2, 1, 7), (1, 1, 7), (1, 2, 7), (1, 2, 6), (1, 2, 5), (1, 2, 4), (1, 3, 4), (0, 3, 4), (0, 2, 4), (0, 2, 5), (0, 1, 5), (1, 1, 5), (2, 1, 5), (2, 2, 5), (2, 2, 6), (3, 2, 6), (3, 3, 6), (3, 3, 7), (4, 3, 7), (5, 3, 7), (5, 2, 7), (6, 2, 7), (6, 1, 7), (5, 1, 7), (5, 1, 6), (5, 1, 5), (6, 1, 5), (6, 1, 4), (6, 0, 4), (6, 0, 3), (6, 0, 2), (5, 0, 2), (4, 0, 2), (3, 0, 2), (2, 0, 2), (2, 1, 2), (2, 1, 1), (3, 1, 1), (3, 2, 1), (3, 2, 0), (4, 2, 0), (4, 3, 0), (3, 3, 0), (2, 3, 0), (2, 2, 0), (1, 2, 0), (1, 2, 1), (1, 2, 2), (1, 3, 2), (1, 3, 3), (1, 4, 3), (1, 4, 2), (2, 4, 2), (3, 4, 2), (3, 5, 2), (3, 6, 2), (4, 6, 2), (4, 5, 2), (5, 5, 2), (5, 4, 2), (5, 4, 1), (6, 4, 1), (6, 3, 1), (7, 3, 1), (7, 3, 2), (7, 4, 2), (7, 4, 1), (7, 4, 0), (7, 5, 0), (6, 5, 0)], [(4, 4, 0), (3, 4, 0), (2, 4, 0), (2, 4, 1), (2, 5, 1), (3, 5, 1), (3, 4, 1), (3, 3, 1), (4, 3, 1), (4, 2, 1), (4, 1, 1), (3, 1, 1), (3, 1, 0)], [(6, 2, 0), (6, 3, 0), (5, 3, 0), (5, 4, 0), (6, 4, 0), (6, 5, 0)], [(6, 2, 0), (7, 2, 0), (7, 1, 0), (6, 1, 0), (5, 1, 0), (5, 1, 1), (5, 0, 1), (5, 0, 0), (4, 0, 0), (4, 1, 0), (3, 1, 0)]]

def amount_crossings(child):
    #
    crossings = 0
    crossing_list = []
    for i in child:
        i = i[1:len(i) - 1]
        for j in i:
           # if j in not nodes:
            crossing_list.append(j)
    crossings = len(crossing_list) - len(set(crossing_list))
    return crossings
    

def is_valid(child):
    # 
    valid = True
    is_valid_list = []
    for i in child:
       for j in range(len(i) - 1):
        is_valid_list.append((i[j], i[j + 1]))
    if len(is_valid_list) > len(set(is_valid_list)):
        valid = False
    else: valid = True
    return valid

def cost(units, crossings):
    return units + 300 * crossings

def fitness(units, crossings):
    ans = cost(units, crossings)
    
    if ans == 0: 
        return 99999
    else: 
        return abs(1/ans)



if __name__ == "__main__":
    print(is_valid(child))
    print(amount_crossings(child))
