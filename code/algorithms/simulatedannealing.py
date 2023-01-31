import random
import math
import itertools
from tqdm import tqdm
from collections import defaultdict

from .PathFinder_Astar_Util import PathFinder_Aster_util as PA_util
from .hillclimber import HillClimber

class SimulatedAnnealing(HillClimber):
    """
    The SimulatedAnnealing class that tries all valid neighbour solutions for the current order.
    If a solution is accepted then the remaining neighbour solutions will not be checked.
    Also sometimes accepts solutions that are worse, depending on the current temperature.
    Most of the functions are similar to those of the HillClimber class, which is why
    we use that as a parent class.
    """
    def __init__(self, netlist, temperature, update_temperature, alpha = None, beta = 1):    
        
        # supercharge this class with Hillclimber class
        super().__init__(netlist)

        # Prepare the oven!
        self.start_temperature = temperature
        self.current_temperature = temperature
        self.iterations = 0
        self.current_iterations = 0
        
        self.alpha = alpha
        self.beta = beta
        
        if update_temperature == "linear":
            self.update_temperature = self.update_temperature_linear
        elif update_temperature == "geometric":
            # check for alpha number
            if not alpha:
                raise Exception("Need alpha arg.")
            # check valid numbers
            if not (0 < alpha < 1):
                raise Exception("Alpha value needs to be between 0 and 1")
            self.update_temperature = self.update_temperature_geometric
        elif update_temperature == "fastDecrease":
            self.update_temperature = self.update_temperature_fastDecrease
        else:
            raise exception("Failed to prepare the oven: invalid update temperature type.")

    def update_temperature_linear(self):
        """
        This function implements a *linear* cooling scheme.
        Temperature will become zero after all iterations passed to the run()
        method have passed.
        """
        self.current_temperature -= (self.start_temperature / self.iterations)
        
    def update_temperature_fastDecrease(self):
        """
        This function implements a *FastDecrease* cooling scheme.
        Temperature will lower based on dividing by the current iteration.
        Adding +1 to avoid divide by 0.
        """
        self.current_temperature = self.current_temperature / (self.current_iterations + 1)  
        
    def update_temperature_geometric(self):
        """
        This function implements a *Exponential* cooling scheme.
        Temperature will lower based on the passed alpha value between 0 and 1.
        """
        self.current_temperature = self.current_temperature * self.alpha
  
    def run(self, iterations):
        """
        Same as Hillclimber but a bit different.
        Also sometimes accepts solutions that are worse, depending on the current
        temperature.
        """
        # set iterations
        self.iterations = iterations
        
        # reset netlist before running
        self.netlist.reset()
        
        # find first solution
        current_path, current_cost = PA_util.get_solution(self.netlist) # added v2 
        
#         print(current_cost)
        
        # reset netlist
        self.netlist.reset()
        
        i = 0

        with tqdm(total=iterations) as pbar:
            while i < iterations:
                # reset netlist
                self.netlist.reset()
                
                # get nearest connection order neighbours
                new_children = self.mutate_child()

                for new_child in new_children:

                    # TODO: more elegant
                    if i >= iterations:
                        break

                    # reset netlist
                    self.netlist.reset()

                    new_path, new_cost = PA_util.find_all_paths(new_child,
                                                                self.netlist)
                    if not new_path:
                        continue
                       
                    i += 1
                    pbar.update(1)

                    new_value = new_cost
                    old_value = current_cost
                    
                    # Calculate the probability of accepting this new connection order
                    delta = self.beta * (new_value - old_value)
                    
                    # prevents overflow if delta is negative and big
                    if -delta > 0:
                        probability = 1.0
                    else:
                        probability = math.exp(-delta / self.current_temperature)
                    
                    # increase current iterations by 1
                    self.current_iterations += 1

                    # Update the temperature
                    self.update_temperature()
                    
                    # Pull a random number between 0 and 1 and see if we accept the new connection order
                    if random.random() < probability:
                        self.current_connection_order = new_child
                        current_path, current_cost = new_path, new_cost
#                         print("Accepted: ", new_cost)
#                         print("Temperature: ", self.current_temperature)
                        break

        return current_path, current_cost
    
    
    @classmethod
    def get_tune_results(cls, netlist, temperatures, alphas, iterations = 50):
        if not (temperatures or alphas):
            raise Exception("Temperature or Alpha sequence must not be empty.")
        
        all_results = defaultdict(dict)
        
        all_results["linear_results"] = {}
        for temperature in temperatures:
#             for alpha in alphas:
            linear_sa = cls(netlist, temperature, "linear")
            path, cost = linear_sa.run(iterations)
            all_results["linear_results"][temperature] = (path, cost)
        
        all_results["fastDecrease_results"] = {}
        for temperature in temperatures:
#             for alpha in alphas:
            linear_sa = cls(netlist, temperature, "fastDecrease")
            path, cost = linear_sa.run(iterations)
            all_results["fastDecrease_results"][temperature] = (path, cost)
       
        for t, a in itertools.product(temperatures, alphas):
            sa = cls(netlist, temperature, "geometric", alpha = a)
            all_results[t][a] = sa.run(iterations)
        
        return all_results
    
    @staticmethod
    def get_best_tuned_result(tune_results):
        first_key = list(tune_results.keys())[0]
        second_key = list(tune_results[first_key].keys())[0]
        winner = tune_results[first_key][second_key]

        # print("winner: ", winner)
        for k, v in tune_results.items():
            for vk, r in v.items():
                if r[1] < winner[1]:
                    first_key = k
                    second_key = vk
                    winner = a[first_key][second_key]
        return first_key, second_key, winner