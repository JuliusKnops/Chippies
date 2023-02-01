"""
config.py

Chippies
Julius Knops, Deniz Mermer, Hidde Brenninkmeijer
Algoritmen & Heuristieken

A configuration file to change parameter values and choose which
algorithm or heuristic is used to solve the netlist problem
"""

###
# Chip and netlist number to solve for
###
from code.classes import netlist
chip_nr: int = 1 
netlist_nr: int = 4
netlist_file = f"data/chip_{chip_nr}/netlist_{netlist_nr}.csv"
print_file = f"data/chip_{chip_nr}/print_{chip_nr}.csv"
Astar_netlist = netlist.Netlist(netlist_file, print_file)

"""
Choose which Heuristic / Algorithm you want to use to solve the problem
[Astar, Hillclimber, SimulatedAnnealing, Random]

Visualize is 3D plot .png-file of solution
experiment calls multiple solutions to calculate average, std dev
iterations is number of iterations used in experiment
"""

# A* parameters
Astar_full_implementation: bool = False 
Astar_sample: int = 1

# Hillclimber parameters
Hillclimber: bool = False
hc_iterations: int = 250 

# Simulated Annealing parameters
SimulatedAnnealing_tune: bool = False 
SA_tune_iterations: int = 30 
SimulatedAnnealing: bool = False 
sa_iterations: int = 100 

# Random algorithm paramater
RandomAlgorithm: bool = False
hardstuck = 100
loopstuck = 10000

# Genetic Algorithm (W.I.P.)
GeneticAlgorithm: bool = False 
MutateChance = 0.1
PopulationSize = 10
NumberOfGenerations = 3

# General settings
Visualize: bool = True 
experiment: bool = True
experiment_duration: int = 3600
iterations: int = 2




# Astar_full_implementation = False
# Astar_sample = 0
# Hillclimber = False
# hc_iterations = 250
# SimulatedAnnealing_tune = False
# SA_tune_iterations = 30
# SimulatedAnnealing = True
# sa_iterations = 250
# RandomAlgorithm = False

# Visualize = True
# experiment = True
# experiment_duration = 3600
# iterations = 10


