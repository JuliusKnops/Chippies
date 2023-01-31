###############################################################
### globally used variables
###############################################################

from code.classes import netlist

"""
Choose which Heuristic / Algorithm you want to use to solve the problem
[Astar, Hillclimber, SimulatedAnnealing, Random]

Visualize is 3D plot .png-file of solution
experiment calls multiple solutions to calculate average, std dev
iterations is number of iterations used in experiment
"""
Astar = True 
Hillclimber = True 
SimulatedAnnealing = True
Random = True

Visualize = True
experiment = True
experiment_duration = 3600
iterations = 10

"""
sampling for chip0,1 
if chip 0 volledige -> kies astar
"""

chip_nr = 0 # loopt van 0 tot en met 2
netlist_nr = 2 # loopt van 1 tot en met 3
netlist_file = f"data/chip_{chip_nr}/netlist_{netlist_nr + 3 * chip_nr}.csv"
print_file = f"data/chip_{chip_nr}/print_{chip_nr}.csv"
Astar_netlist = netlist.Netlist(netlist_file, print_file)