import random
import copy
import tqdm

from .find_paths import *

class HillClimber(object):
    """
    An iterative algorithm that starts with an first solution to the problem, 
    by using the first connection order given back from 
    netlist.get_connection_tuples().
    Then attempts to find a better solution by making an incremental change to 
    the order. In this case it will find all neighbour solutions and try them
    all out. If a better solution is found, replaces the current solution or
    connection order with the new better one.
    """

    def __init__(self, netlist):
        # Initialize the board
        self.netlist = netlist
        # First connection order and length
        self.current_connection_order = netlist.connection_tuples
        self.len_connection_order = len(self.current_connection_order)
        # archive for mutate_child_by_random_swap
        self.used_permutation = set()
        # add first solution order
        self.used_permutation.add(tuple(self.current_connection_order))
    
    def mutate_child(self):
        """
        Returns mutated children by finding all nearest neighbour solutions.
        """
        nearest_neighbours = []
        order = self.current_connection_order
        
        for i in range(len(order)):
            for j in range(i + 1, len(order)):
                neighbour = copy.copy(order)
                neighbour[i] = order[j]
                neighbour[j] = order[i]
                nearest_neighbours.append(neighbour)
        return nearest_neighbours
        
    def mutate_child_by_random_swap(self):
        """
        Mutates given child by randomly swapping 2 connection orders.
        Returns a unique mutated child without alterning object attributes.
        """
        
        # create unused child
        for i in range(5000):
            # pick first swap index
            i = random.randint(0, self.len_connection_order - 1)

            # pick different second swap index
            j = i
            while j == i:
                j = random.randint(0, self.len_connection_order - 1)

            # swap em
            child = copy.copy(self.current_connection_order)
            child[i] = self.current_connection_order[j]
            child[j] = self.current_connection_order[i]
           
            # if unused child, break
            if tuple(child) not in self.used_permutation:
                self.used_permutation.add(tuple(child))
                break
                
        else:
            raise Exception("Failed to find a child!")

        return child
        
    def run(self, iterations):
        """
        Runs the algororithms i times, with i being the given number of
        iterations.
        Returns the best found path and its cost.
        """
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
                if new_cost < current_cost:
                    self.current_connection_order = new_child
                    current_path, current_cost = new_path, new_cost
                    print(new_cost)

                # reset netlist
                self.netlist.reset()

        return current_path, current_cost