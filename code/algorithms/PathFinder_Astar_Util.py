from tqdm import tqdm

import itertools
import more_itertools as mit
import math
import random
import warnings

from . import Astar
from . import dijkstra

class PathFinder_Aster_util(object):
    # sample needs to be equal or lower than that var
    # Example: pop is 100, then the sample is 5 or lower.
    population_sample_size_ratio = 0.05
    
    @staticmethod
    def find_all_paths( all_connections, netlist: object, as_objects = False, 
                        PathFinder = Astar.PathFinder_Astar, 
                        Node = Astar.Node_Astar) -> tuple:
        """
        Find all paths in the given order in all_connections using the given
        netlist and algorithm to use.
        Once a path is found adds the connections to the netlist.

        all_connections structure: [ (start_node, end_node), 
                                     (start_node, end_node)...]
        Algorithm to use dictated by PathFinder and Node (see Astar.py and 
        dijkstra.py)
        """
        all_paths = []
        total_cost = 0

        # get all paths of each connection and sum the total cost
        for connection in all_connections:
            start_node, end_node = connection
            path = PathFinder(Node(*start_node), Node(*end_node), Node = Node)
            
            # return none if no path found
            if not path.path:
                return (None, None)

            all_paths.append(path)
            total_cost += path.cost

            # add connections to used_connections
            for i in range( (len(path.path)-1) ):
                wire = frozenset({path.path[i], path.path[i+1]})
                netlist.used_connections.add(wire)
                netlist.n += 1

        # returns paths as PathFinder objects, else as list of paths
        if as_objects:
            return all_paths, total_cost

        return [pf.path for pf in all_paths], total_cost
    
    @classmethod
    def find_cheapest_path( cls, netlist: object, 
                            PathFinder =Astar.PathFinder_Astar, 
                            Node = Astar.Node_Astar) -> tuple:
        """
        Finds the cheapest path by trying all possible permutations of 
        connection order. Or in other words: for which connections to find a 
        path first.
        """
        
        # reset visited nodes before starting
        # NOTE: probs not needed
        netlist.reset()

        all_connections = netlist.connection_tuples

        # create generator for all orders to connect the connections
        all_connections_permutations = itertools.permutations(all_connections)

        # get total number of permutations
        all_permutation_length = math.factorial(len(all_connections))

        # find first solution
        current_path, current_cost = cls.get_random_solution(netlist)

        # reset netlist
        netlist.reset()

        current_path, current_cost = cls.get_best_path(
                                                current_path, current_cost,
                                                netlist,
                                                all_connections_permutations,
                                                all_permutation_length,
                                                PathFinder = PathFinder, 
                                                Node = Node)
        return current_path, current_cost
    
    @classmethod
    def find_cheapest_path_from_sample( cls, netlist: object,
                                        random_sample_max_iter: int,
                                        PathFinder = Astar.PathFinder_Astar, 
                                        Node = Astar.Node_Astar ) -> tuple:
        """
        Finds the cheapest path by trying all permutations from a sample of size
        random_sample_max_iter
        """
        
        # reset visited nodes before starting
        # NOTE: probs not needed
        netlist.reset()

        all_connections = netlist.connection_tuples

        # get all orders to connect the connections
        all_connections_permutations = itertools.permutations(all_connections)

        # get total number of permutations
        all_permutation_length = math.factorial(len(all_connections))
        
        # see if we can even fill the list
        if all_permutation_length < random_sample_max_iter:
            raise Exception("not enough permutations")

        # raise warning if sample size not beneath ratio treshold
        ratio_size = cls.population_sample_size_ratio * all_permutation_length
        if ratio_size <= random_sample_max_iter:
            msg = ( "Inappropriate usage of function detected: "+
                    f"Sample size is not {cls.population_sample_size_ratio }%" +
                    "or lower.")
            warnings.warn(msg)

        # find first solution
        current_path, current_cost = cls.get_random_solution(netlist)

        # reset netlist
        netlist.reset()
        
        # sample
        random_permutations = set()

        # create random list of permutations from generator
        while len(random_permutations) < random_sample_max_iter:
            rp = mit.random_permutation(all_connections)
            random_permutations.add(rp)

        random_permutations = tuple(random_permutations)

        current_path, current_cost = cls.get_best_path(
                                                current_path, current_cost,
                                                netlist,
                                                random_permutations,
                                                len(random_permutations),
                                                PathFinder = PathFinder, 
                                                Node = Node)
        return current_path, current_cost

    @classmethod
    def get_random_solution(cls, netlist: object, 
                            PathFinder = Astar.PathFinder_Astar, 
                            Node = Astar.Node_Astar) -> tuple:
        """
        Returns random solution.
        Does this by trying different random connection orders until first one
        found.
        """
        all_connections = netlist.connection_tuples

        # get all orders to connect the connections
        all_connections_permutations = itertools.permutations(all_connections)

        # get total number of permutations
        all_permutation_length = math.factorial(len(all_connections))

        # Find the first path and cost
        for i in range(10000):

            # reset visited nodes
            netlist.reset()

            # choice random permutation, includes all_connection
            rp = mit.random_permutation(all_connections)
            netlist.connection_tuples = list(rp)
            current_path, current_cost = cls.find_all_paths(
                                                    rp,
                                                    netlist,
                                                    PathFinder = PathFinder,
                                                    Node = Node
                                                            )
            if current_path:
                return current_path, current_cost


        # if it fails to find a first path too many times:
        # iterate until first path found
        if not current_path:
            # go through each order and find the cheapest path
            for permutation in all_connections_permutations:

                # reset visited nodes
                netlist.reset()

                new_path, new_cost = cls.find_all_paths(
                                                    permutation, netlist,
                                                    PathFinder=PathFinder, 
                                                    Node = Node
                                                        )
                if new_path:
                    current_path = new_path
                    current_cost = new_cost
                    netlist.connection_tuples = permutation
                    break

                # reset visited nodes
                netlist.reset()

        return current_path, current_cost

    @classmethod
    def get_best_path(cls, current_path: list, current_cost: int,
                        netlist: object,
                        permutations: itertools.permutations,
                        total: int,
                        PathFinder = Astar.PathFinder_Astar, 
                        Node = Astar.Node_Astar) -> tuple:
        """
        Find best path from the given permutations iterable. Can be a genetor or
        a list from the itertools.permutation generator.
        """
        # go through each order and find the cheapest path
        for permutation in tqdm(permutations, total = total):

            # reset visited nodes
            netlist.reset()

            new_path, new_cost = cls.find_all_paths(permutation, netlist,
                                                    PathFinder=PathFinder, 
                                                    Node = Node)

            # if not path, skip
            if not new_path:
                continue

            if new_cost < current_cost:
                current_path = new_path
                current_cost = new_cost

        return current_path, current_cost
