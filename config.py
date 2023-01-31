###############################################################
### globally used variables
###############################################################

from code.classes import netlist


Astar = True 
Hillclimber = True 
SimulatedAnnealing = True
Random = True
Visualize = True

experiment = True
iterations = 10



chip_nr = 0 # loopt van 0 tot en met 2
netlist_nr = 2 # loopt van 1 tot en met 3
netlist_file = f"data/chip_{chip_nr}/netlist_{netlist_nr + 3 * chip_nr}.csv"
print_file = f"data/chip_{chip_nr}/print_{chip_nr}.csv"
Astar_netlist = netlist.Netlist(netlist_file, print_file)