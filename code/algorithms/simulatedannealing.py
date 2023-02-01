import random
import math
import itertools
from tqdm import tqdm
from collections import defaultdict

from .PathFinder_Astar_Util import PathFinder_Aster_util as PA_util
from .hillclimber import HillClimber

class SimulatedAnnealing(HillClimber):
    """
    The SimulatedAnnealing class that tries all valid neighbour solutions for 
    the current order.
    If a solution is accepted then the remaining neighbour solutions will 
    not be checked.
    Also sometimes accepts solutions that are worse, depending on the current 
    temperature.
    Most of the functions are similar to those of the HillClimber class, which 
    is why we use that as a parent class.
    """
    def __init__(self, netlist: object, temperature: int,
                    update_temperature: str, alpha = None, beta = 1) -> None:  
        
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
            raise Exception("Invalid update_temperature arg")

    def update_temperature_linear(self) -> None:
        """
        This function implements a *linear* cooling scheme.
        Temperature will become zero after all iterations passed to the run()
        method have passed.
        """
        self.current_temperature -= (self.start_temperature / self.iterations)
        
    def update_temperature_fastDecrease(self) -> None:
        """
        This function implements a *FastDecrease* cooling scheme.
        Temperature will lower based on dividing by the current iteration.
        Adding +1 to avoid divide by 0.
        """
        self.current_temperature /= (self.current_iterations + 1)  
        
    def update_temperature_geometric(self) -> None:
        """
        This function implements a *Exponential* cooling scheme.
        Temperature will lower based on the passed alpha value between 0 and 1.
        """
        self.current_temperature = self.current_temperature * self.alpha

    def evaluate_result(self, current_cost: int, new_cost: int) -> None:
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

        return random.random() < probability  
    
    @classmethod
    def get_tune_results(cls, netlist: object, temperatures: list, alphas: list,
                            iterations = 50) -> None:
        if not (temperatures or alphas):
            raise Exception("Temperature or Alpha sequence must not be empty.")
        
        all_results = defaultdict(dict)
        
        # gather results for linear
        all_results["linear_results"] = {}
        for temperature in temperatures:
            linear_sa = cls(netlist, temperature, "linear")
            path, cost = linear_sa.run(iterations)
            all_results["linear_results"][temperature] = (path, cost)
        
        # gather results for fastDecrease
        all_results["fastDecrease_results"] = {}
        for temperature in temperatures:
            linear_sa = cls(netlist, temperature, "fastDecrease")
            path, cost = linear_sa.run(iterations)
            all_results["fastDecrease_results"][temperature] = (path, cost)

        # gather results for temperatures and alphas (unique) combinations
        for t, a in itertools.product(temperatures, alphas):
            sa = cls(netlist, temperature, "geometric", alpha = a)
            all_results[t][a] = sa.run(iterations)
        
        return all_results
    
    @staticmethod
    def get_best_tuned_result(tune_results: defaultdict) -> tuple:
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