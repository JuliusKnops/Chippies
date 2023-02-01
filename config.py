"""
config.py

Chippies
Julius Knops, Deniz Mermer, Hidde Brenninkmeijer
Algoritmen & Heuristieken

A configuration file to change parameter values and choose which
algorithm or heuristic is used to solve the netlist problem
"""

from code.classes import netlist
chip_nr: int = 2 
netlist_nr: int = 9
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
# Astar_full_implementation: bool = False # True or False
# Astar_sample: int = 0 # int between 0 - 1000000


# Hillclimber: bool = True # True or False
# hc_iterations: int = 250 # int between 0 - 1000000


# SimulatedAnnealing_tune: bool = False # True or False
# SA_tune_iterations: int = 30 # int between 0 - 1000000
# SimulatedAnnealing: bool = False # True or False

# sa_iterations: int = 100 # int between 0 - 1000000
# Random: bool = False # True or False


# Visualize: bool = True # True or False
# experiment: bool = True
# experiment_duration: int = 3600
# iterations: int = 10
# ###

Astar_full_implementation = False
Astar_sample = 0
Hillclimber = False
hc_iterations = 250
SimulatedAnnealing_tune = False
SA_tune_iterations = 30
SimulatedAnnealing = True
sa_iterations = 250
Random = False

Visualize = True
experiment = True
experiment_duration = 3600
iterations = 10

"""
sampling for chip0,1 
if chip 0 volledige -> kies astar
"""

