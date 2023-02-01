"""
main.py

Chippies
Julius Knops, Deniz Mermer, Hidde Brenninkmeijer
Algoritmen & Heuristieken

Main file that executes the correct functions given by user 
input in config.py
"""

from code.algorithms import Astar
from code.algorithms import hillclimber as hc
from code.algorithms import simulatedannealing as sa
from code.algorithms import random_algo

from code.algorithms.PathFinder_Astar_Util import ( PathFinder_Aster_util as 
                                                    PA_util )


from code.classes import netlist

from code.visualisation import visualisation

import config
import csv
import json

if __name__ == "__main__":

    config.netlist_file = ( f"data/chip_{config.chip_nr}/netlist_"+
                    f"{config.netlist_nr + 3 * config.chip_nr}.csv" )
    config.print_file = f"data/chip_{config.chip_nr}/print_{config.chip_nr}.csv"
    config.Astar_netlist = netlist.Netlist( config.netlist_file, 
                                            config.print_file)

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
        best_solution = PA_util.find_cheapest_path(
                                            config.Astar_netlist, 
                                            PathFinder = Astar.PathFinder_Astar, 
                                            Node = Astar.Node_Astar)
        fn = ("Astar_best_solution_"+str(config.chip_nr)+"_"+
                str(config.netlist_nr)+".json")
        with open(fn, "w") as outfile:
            json.dump(best_solution, outfile)

    if config.Astar_sample:
        solutions = {}
        fn = ("Astar_sample_"+str(config.chip_nr)+"_"+str(config.netlist_nr)+
                ".json")
        for i in range(config.Astar_sample_generate_count):
            random_solution = PA_util.find_cheapest_path_from_sample(
                                    config.Astar_netlist, 
                                    PathFinder=Astar.PathFinder_Astar, 
                                    Node=Astar.Node_Astar, 
                                    random_sample_max_iter = config.Astar_sample
                                        )
            solutions[i] = random_solution
            with open(fn, "w") as outfile:
                json.dump(solutions, outfile)

    if config.Hillclimber:
        solutions = {}
        fn = ( "Hillclimber_sample_"+str(config.chip_nr)+"_"+
                str(config.netlist_nr)+".json" )
        for i in range(config.hc_generate_count):
            hillclimber = hc.HillClimber(config.Astar_netlist)
            random_solution = hillclimber.run(iterations = config.hc_iterations)
            solutions[i] = random_solution
            with open(fn, "w") as outfile:
                json.dump(solutions, outfile)
    
    if config.SimulatedAnnealing_tune:

        fn_r = ("tune_results_"+str(config.chip_nr)+"_"+str(config.netlist_nr)+
                ".json")
        fn_br = ("best_tune_results"+str(config.chip_nr)+"_"+
                str(config.netlist_nr)+".json")

        all_tune_results = {}
        best_tune_results = {}

        for i in range(config.sa_tune_generate_count):
            tune_results = sa.SimulatedAnnealing.generate_tune_results(
                                        config.Astar_netlist, 
                                        [16384, 3600, 512], 
                                        [.9, .96, .75, .5], 
                                        iterations = config.sa_tune_iterations)
            get_best_tuned_result = sa.SimulatedAnnealing.get_best_tuned_result(
                                                                tune_results)
            all_tune_results[i] = tune_results
            best_tune_results[i] = best_tune_results
            with open(fn_r, "w") as outfile:
                json.dump(all_tune_results, outfile)

            with open(fn_br, "w") as outfile:
                json.dump(all_tune_results, outfile)

    if config.SimulatedAnnealing:
        solutions = {}
        fn = ( "SimulatedAnnealing_sample_"+str(config.chip_nr)+"_"+
                str(config.netlist_nr)+".json" )
        for i in range(config.sa_generate_count):
            simulated_annealing = sa.SimulatedAnnealing(config.Astar_netlist, 
                                                        16384, "geometric", 
                                                        alpha = .96)
            random_solution = simulated_annealing.run(
                                                iterations=config.sa_iterations)
            solutions[i] = random_solution
            with open(fn, "w") as outfile:
                json.dump(solutions, outfile)

    
