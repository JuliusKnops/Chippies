###############################################################
### globally used variables
###############################################################

from code.classes import netlist

grid_rows = 3
grid_cols = 3
grid_layers = 1
chip_nr = 0 # loopt van 0 tot en met 2
netlist_nr = 1 # loopt van 1 tot en met 3
netlist_file = f"data/chip_{chip_nr}/netlist_{netlist_nr + 3 * chip_nr}.csv"
print_file = f"data/chip_{chip_nr}/print_{chip_nr}.csv"
Astar_netlist = netlist.Netlist(netlist_file, print_file)