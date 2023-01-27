import random
import math
import tqdm

from .find_paths import *
from .hillclimber import HillClimber

class SimulatedAnnealing(HillClimber):
    """
    The SimulatedAnnealing class that tries all valid neighbour solutions for the current order.
    Each improvement is saved, but the remaining next neighbour solutions are still checked.
    Also sometimes accepts solutions that are worse, depending on the current temperature.
    Most of the functions are similar to those of the HillClimber class, which is why
    we use that as a parent class.
    """
    def __init__(self, netlist, temperature=1):
        # supercharge this class with Hillclimber class
        super().__init__(netlist)

        # Prepare the oven
        self.start_temperature = temperature
        self.current_temperature = temperature
        self.iterations = 0

    def update_temperature(self):
        """
        This function implements a *linear* cooling scheme.
        Temperature will become zero after all iterations passed to the run()
        method have passed.
        Different cooling schemes will be used during experimenting this weekend.
        """
        self.current_temperature = self.current_temperature - (self.start_temperature / self.iterations)

        # Exponential would look like this:
        # alpha = 0.99
        # self.T = self.T * alpha

        # where alpha can be any value below 1 but above 0

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
        
        current_path, current_cost = find_all_paths(self.current_connection_order,
                                                    self.netlist)
        print(current_cost)
        
        # reset netlist
        self.netlist.reset()
    
        for i in tqdm(range(iterations)):
            # get nearest connection order neighbours
            new_children = self.mutate_child()

            for new_child in tqdm(new_children):
                new_path, new_cost = find_all_paths(new_child,
                                                    self.netlist)
                
                new_value = new_cost
                old_value = current_cost

                # Calculate the probability of accepting this new connection order
                delta = new_value - old_value
                probability = math.exp(-delta / self.current_temperature)
                
                # Pull a random number between 0 and 1 and see if we accept the new connection order
                if random.random() < probability:
                    self.current_connection_order = new_child
                    current_path, current_cost = new_path, new_cost
                    print(new_cost)
                
                # lower iterations to go by 1
                self.iterations -= 1
                
                # reset netlist
                self.netlist.reset()
            
            # Update the temperature
            self.update_temperature()

        return current_path, current_cost