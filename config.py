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
chip_nr: int = 0 # loopt van 0 tot en met 2
netlist_nr: int = 1 # loopt van 1 tot en met 3
netlist_file = None
print_file = None
Astar_netlist = None

"""
Choose which Heuristic / Algorithm you want to use to solve the problem
[Astar, Hillclimber, SimulatedAnnealing, Random]

Visualize is 3D plot .png-file of solution
experiment calls multiple solutions to calculate average, std dev
iterations is number of iterations used in experiment
"""

# A* parameters
Astar_full_implementation: bool = False 
Astar_sample_generate_count: int = 10
Astar_sample: int = 0

# Hillclimber parameters
Hillclimber: bool = False
hc_generate_count: int = 25
hc_iterations: int = 250 

# Simulated Annealing parameters
SimulatedAnnealing_tune: bool = False 
sa_tune_iterations: int = 30
sa_tune_generate_count: int = 25
SimulatedAnnealing: bool = False
sa_generate_count: int = 25
sa_iterations: int = 100

# random netlist parameters
random_netlist: bool = False
gates_max: int = 7
x_max: int = 12
y_max: int = 12
connections_max: int = 7

# Random algorithm parameter
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



