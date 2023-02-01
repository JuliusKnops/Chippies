"""
main.py

Chippies
Julius Knops, Deniz Mermer, Hidde Brenninkmeijer
Algoritmen & Heuristieken

Main file that executes the correct functions given by user 
input in config.py
"""

from code.algorithms import Astar
from code.algorithms import dijkstra
from code.algorithms import hillclimber as hc
from code.algorithms import simulatedannealing as sa
from code.algorithms import genetic_algorithm
from code.algorithms import genetic
from code.algorithms import move_random
from code.algorithms import random_algo

from code.algorithms import PathFinder_Astar_Util as PA_util

from code.classes import gates
from code.classes import netlist

from code.visualisation import visualisation

import config
import timeit
import time
import subprocess
import csv
import json

if __name__ == "__main__":

    if config.RandomAlgorithm:
        if config.experiment:
            for i in range(config.iterations):
                
                solution_cost, solution_connections, solution_gates = random_algo.get_randomize_solution(config.Astar_netlist)
                
                with open(f'chip_{config.chip_nr}_{config.netlist_nr}.csv', 'a', encoding='UTF8') as f:
                    writer = csv.writer(f)
                    for row in [[solution_cost, solution_connections]]:
                        writer.writerow(row)
                

            visualisation.create_histogram(config.chip_nr, config.netlist_nr)

        solution_cost, solution_connections, solution_gates = random_algo.get_randomize_solution(config.Astar_netlist)

        if config.Visualize:
            visualisation.visualisation(solution_connections, solution_gates, config.chip_nr)
    
    if config.Astar_full_implementation:
        best_solution = PA_util.PathFinder_Aster_util.find_cheapest_path( config.Astar_netlist, 
                                                    PathFinder=Astar.PathFinder_Astar, 
                                                    Node=Astar.Node_Astar)
        fn = "Astar_best_solution_"+str(config.chip_nr)+"_"+str(config.netlist_nr)+".json"
        with open(fn, "w") as outfile:
            json.dump(best_solution, outfile)

    if config.Astar_sample:
        solutions = {}
        for i in range(1000):
            random_solution = PA_util.PathFinder_Aster_util.find_cheapest_path_from_sample(config.Astar_netlist, 
                                                                                            PathFinder=Astar.PathFinder_Astar, 
                                                                                            Node=Astar.Node_Astar, random_sample_max_iter = config.Astar_sample)
            solutions[i] = random_solution
            fn = "Astar_sample_"+str(config.chip_nr)+"_"+str(config.netlist_nr)+".json"
            with open(fn, "w") as outfile:
                json.dump(solutions, outfile)

    if config.Hillclimber:
        solutions = {}
        for i in range(20):
            hillclimber = hc.HillClimber(config.Astar_netlist)
            random_solution = hillclimber.run(iterations = config.hc_iterations)
            solutions[i] = random_solution
            fn = "Hillclimber_sample_"+str(config.chip_nr)+"_"+str(config.netlist_nr)+".json"
            with open(fn, "w") as outfile:
                json.dump(solutions, outfile)

    if config.SimulatedAnnealing_tune:
        tune_results = sa.SimulatedAnnealing.get_tune_results(
                                                            config.Astar_netlist, 
                                                            [16384, 3600, 512], 
                                                            [.9, .75, .5], 
                                                            iterations = config.SA_tune_iterations)
        get_best_tuned_result = sa.SimulatedAnnealing.get_best_tuned_result(tune_results)
        print(get_best_tuned_result)

    if config.SimulatedAnnealing:
        solutions = {}
        for i in range(25):
            simulated_annealing = sa.SimulatedAnnealing(config.Astar_netlist, 16384, "geometric", alpha = .96)
            random_solution = simulated_annealing.run(iterations=config.sa_iterations)
            solutions[i] = random_solution
            fn = "SimulatedAnnealing_sample_"+str(config.chip_nr)+"_"+str(config.netlist_nr)+".json"
            with open(fn, "w") as outfile:
                json.dump(solutions, outfile)
        


    # chip_nr = 0 # loopt van 0 tot en met 2
    # netlist_nr = 3 # loopt van 1 tot en met 3
    
    # netlist_file = f"data/chip_{chip_nr}/netlist_{netlist_nr + 3 * chip_nr}.csv"
    # print_file = f"data/chip_{chip_nr}/print_{chip_nr}.csv"
    
    # netlists = netlist.Netlist(netlist_file, print_file)
    
    
    # # print(random_algo.get_randomize_solution(netlists))

    # print(genetic.create_new_pop(netlists))

    # netlist_nr = 1
    # for chip_nr in range(3):
    #     netlist_file = f"data/chip_{chip_nr}/netlist_{netlist_nr + 3 * chip_nr}.csv"
    #     print_file = f"data/chip_{chip_nr}/print_{chip_nr}.csv"
    #     netlists = netlist.Netlist(netlist_file, print_file)
    #     found_solution, found_cost = random_algo.get_randomize_solution(netlists)

    #     header = ['solution']
    #     with open(f'chip_{chip_nr}.csv', 'w', encoding='UTF8') as f:
    #         writer = csv.writer(f)
    #         writer.writerow(header)
    #         # for row in found_solution:
    #         writer.writerow([found_cost])
    #         writer.writerow([found_solution])
        
    #     print(f"SOLVED {chip_nr}")




    """
    ###
    # VISUALISATIE RESULTATEN
    ###
    # import csv
    # csv_values = []
    # for batchID in range(3):
    #     print(f"BATCH RUN: {batchID}")
    #     batch_values = []
    #     BestCost = 10000
    #     WorstCost = 0
    #     RunCost = []
    #     n_runs = 2500
    #     AverageCost = 0
    #     StdDev = 0
    #     for runID in range(n_runs):
    #         if runID % 100 == 0:
    #             print(f"RUN: {runID}")
    #         cost, solution = random_algo.get_randomize_solution(netlist)
    #         RunCost.append(cost)
    #         if cost < BestCost:
    #             BestSolution = solution
    #         BestCost = min(BestCost, cost)
    #         WorstCost = max(WorstCost, cost)
            
    #     StdDev = np.std(RunCost)
    #     AverageCost = sum(RunCost) / len(RunCost)
    #     batchRun = [batchID, AverageCost, StdDev, BestCost, WorstCost, BestSolution]
    #     csv_values.append(batchRun)
    

    # header = ['batchID', 'AverageCost', 'StdDev', 'BestCost', 'WorstCost', 'runID', 'runCost']
    # with open('BatchRuns.csv', 'w', encoding='UTF8') as f:
    #     writer = csv.writer(f)
    #     writer.writerow(header)
    #     for row in csv_values:
    #         writer.writerow(row)
    """








    



    # visualisation.visualisation( netlist.gate_locations, chip_nr)
    # print(f"netlist.gates = {netlist.gates}")

    # for chip in netlist.gates:
    #     print(chip, netlist.gates[chip].x, netlist.gates[chip].y, netlist.gates[chip].connections)
    
    #move_random(netlist)
    # print(move_random.greedy(netlist))

    # print(find_cheapest_path(config.Astar_netlist, PathFinder=Astar.PathFinder_Astar, Node=Astar.Node_Astar))
    # print(dijkstra.PathFinder_dijkstra(config.Astar_netlist.connection_tuples))

    # n = 10

    # result = timeit.timeit(stmt='find_cheapest_path(config.Astar_netlist, PathFinder=dijkstra.PathFinder_dijkstra, Node=dijkstra.Node_dijkstra)', globals=globals(), number=n)
    # result2 = timeit.timeit(stmt='find_cheapest_path(config.Astar_netlist, PathFinder=Astar.PathFinder_Astar, Node=Astar.Node_Astar)', globals=globals(), number=n)
    
    # print(f"Execution time of Astar is {result / n} seconds")
    # print(f"Execution time of dijkstra is {result2 / n} seconds")

    # hillclimber = hc.HillClimber(config.Astar_netlist)
    # print(hillclimber.run(1))

    # simulatedannealing = sa.SimulatedAnnealing(config.Astar_netlist)
    # print(simulatedannealing.run(1))



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
    
