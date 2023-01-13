import math
import sys 
from decimal import *

# Max float value
# print(sys.float_info.max)

"""getcontext().prec = 6
print(Decimal(1) / Decimal(7))
#Decimal('0.142857')
getcontext().prec = 28
print(Decimal(1) / Decimal(7))
#Decimal('0.1428571428571428571428571429')"""

# Dimensions of chip
length = 18
width = 18
height = 8

# max number of nodes placed on chip
number_of_nodes = 50

# number of edges
number_of_edges = -length*width - length*height - width*height + 3*width*height*length

# number of maximum nodes
max_nodes = length*width*height


def sigma_nodes(first, number_of_nodes, max_nodes):
    total = 0
    for i in range(first, number_of_nodes + 1):
        total += Decimal((math.factorial(max_nodes))/(math.factorial(i) * math.factorial(max_nodes-i)))
    return total

total_comb_nodes = sigma_nodes(0, number_of_nodes, max_nodes)
print(total_comb_nodes)


def sigma_edges(first, n_edges):
    total = 0
    for i in range(first, n_edges+1):
        total += Decimal(math.factorial(n_edges)//((math.factorial(i)) * (math.factorial(n_edges - i))))
    return total

total_comb_edges = sigma_edges(0, number_of_edges)
print(total_comb_edges)

print(Decimal(total_comb_edges * total_comb_nodes))

"""
print(len(str(total_comb_edges)))

print(f"Total State Space size = {total_comb_nodes * total_comb_edges}")"""
