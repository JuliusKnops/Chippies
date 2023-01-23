from code.algorithms import Astar
from code.algorithms import dijkstra
from code.algorithms import genetic_algorithm
from code.algorithms import genetic
from code.algorithms import move_random
from code.algorithms import random_algo

from code.algorithms.find_paths import find_cheapest_path

from code.classes import gates
from code.classes import netlist

from code.visualisation import visualisation

import config
import timeit

import config

if __name__ == "__main__":
    chip_nr = 0 # loopt van 0 tot en met 2
    netlist_nr = 1 # loopt van 1 tot en met 3

    netlist_file = f"data/chip_{chip_nr}/netlist_{netlist_nr + 3 * chip_nr}.csv"
    print_file = f"data/chip_{chip_nr}/print_{chip_nr}.csv"
    
    netlist = netlist.Netlist(netlist_file, print_file)
    

    # print(f"netlist.gates = {netlist.gates}")

    # for chip in netlist.gates:
    #     print(chip, netlist.gates[chip].x, netlist.gates[chip].y, netlist.gates[chip].connections)
    
    print(random_algo.get_randomize_solution(netlist))
    
    
    
    #move_random(netlist)
    # print(move_random.greedy(netlist))

    # print(find_cheapest_path(config.Astar_netlist, PathFinder=Astar.PathFinder_Astar, Node=Astar.Node_Astar))
    # print(dijkstra.PathFinder_dijkstra(config.Astar_netlist.connection_tuples))

    # n = 10

    # result = timeit.timeit(stmt='find_cheapest_path(config.Astar_netlist, PathFinder=dijkstra.PathFinder_dijkstra, Node=dijkstra.Node_dijkstra)', globals=globals(), number=n)
    # result2 = timeit.timeit(stmt='find_cheapest_path(config.Astar_netlist, PathFinder=Astar.PathFinder_Astar, Node=Astar.Node_Astar)', globals=globals(), number=n)
    
    # print(f"Execution time of Astar is {result / n} seconds")
    # print(f"Execution time of dijkstra is {result2 / n} seconds")

"""
    grid_rows = 3
    grid_cols = 3
    grid_layers = 1
    # 2x2 grid with only 1 layer
    grid = [
            [ # start of layer
            [[0, 0, 0], [0, 1, 0]], # X-axis row 1 
            [[1, 0, 0], [1, 1, 0]]  # X-axis row 2
                 ] # end of layer
                ]
    start = Node(0, 0, 0)
    end = Node(2, 2, 0)

    start01 = Node(1, 0, 0)
    end01 = Node(1, 1, 0)

    # Astar_netlist = Netlist(netlist_file, print_file)
    #print("\n")
    # Astar_netlist.used_connections.add("test")
    main.Astar_netlist.gate_locations.update(( (0, 0, 0), (1, 0, 0), (2, 2, 0), (1, 1, 0) ))
    print(find_all_paths([ (start, end), (start01, end01) ]))
    # print(main.Astar_netlist.used_connections)"""
    
