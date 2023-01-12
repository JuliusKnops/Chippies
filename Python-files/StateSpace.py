"""
Calculates the size of StateSpace for a given chip / grid.
First calculates the sum of total number of combinations of placing 0 to number_of_nodes on the grid
Second calculates the sum of total number of combinations of placing edges on the grid
Third multiply values of both functions to get the total set of combinations possible

Assumptions of placement:
- Nodes can be placed on every layer of the chip
- Segments of connection between nodes can cross
"""

# libraries used to get faculty (!) and Decimal function to work with large values
import math
from decimal import *

# Dimensions of chip / grid
length = 18
width = 18
height = 8

p = 5**2023
print(len(str(p)))

# max number of nodes placed on chip
number_of_nodes = 50

# number of edges on given chip / grid
number_of_edges = -length*width - length*height - width*height + 3*width*height*length

# number of maximum nodes on given chip / grid
max_nodes = length*width*height

# Placing nodes on the grid has no value in order placing the nodes and
# repetition is not allowed (not placing more than one nodes on the same spot)
# Thus using the following function: n! / (r! * (n - r)!)
# where:
# n = number of positions for each node while placing
# r = number of nodes that need to be placed on the grid
# This function takes the sum of number of combinations of 0 through 50 nodes. 
def sigma_nodes(first, number_of_nodes, max_nodes):
    total = 0
    for i in range(first, number_of_nodes + 1):
        total += Decimal((math.factorial(max_nodes))/(math.factorial(i) * math.factorial(max_nodes-i)))
    return total

# Placing edges on the grid has no value in order placing the edges and
# repetition is not allowed (not placing more than one nodes on the same spot)
# Thus using the following function: n! / (r! * (n - r)!)
# where:
# n = number of positions for each edge while placing
# r = number of edges that need to be placed on the grid
# This function takes the sum of number of combinations of 0 through the total number of edges. 
def sigma_edges(first, n_edges):
    total = 0
    for i in range(first, n_edges+1):
        total += Decimal(math.factorial(n_edges)//((math.factorial(i)) * (math.factorial(n_edges - i))))
    return total

# Calculate the size of both sets and multiply them to get the total state-space
total_comb_nodes = sigma_nodes(0, number_of_nodes, max_nodes)
print(total_comb_nodes)

total_comb_edges = sigma_edges(0, number_of_edges)
print(total_comb_edges)

print(Decimal(total_comb_edges * total_comb_nodes))

