from . import Astar
from . import dijkstra

import itertools

def find_all_paths( all_connections, netlist, as_objects = False, 
                    PathFinder = Astar.PathFinder_Astar, Node = Astar.Node_Astar):
    """
    Find all paths in the given order in all_connections using the given
    netlist and algorithm to use.

    all_connections structure: [ (start_node, end_node), (start_node, end_node)...]
    Algorithm to use dictated by PathFinder and Node (see Astar.py and dijkstra.py)
    """
    all_paths = []
    total_cost = 0

    # get all paths of each connection and sum the total cost
    for connection in all_connections:
        start_node, end_node = connection
        path = PathFinder(Node(*start_node), Node(*end_node), Node = Node)
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

def find_cheapest_path( netlist, PathFinder = Astar.PathFinder_Astar, 
                        Node = Astar.Node_Astar):
    """
    Finds the cheapest path by trying all possible permutations of connection
    order. Or in other words: for which connections to find a path first. 
    """

    all_connections = netlist.connection_tuples
    # get all orders to connect the connections
    all_connections_permutations = tuple(itertools.permutations(all_connections))

    # Find the first path and cost
    current_path, current_cost = find_all_paths(all_connections_permutations[0],
                                                netlist,
                                                PathFinder=PathFinder,
                                                Node = Node)

    print(current_cost)

    # reset netlist
    netlist.reset()

    # go through each order and find the cheapest path
    for permutation in all_connections_permutations[1:]:
        new_path, new_cost = find_all_paths(permutation, netlist,
                                            PathFinder=PathFinder, Node = Node)
        if new_cost < current_cost:
            current_path = new_path
            current_cost = new_cost
            print(current_cost)

        # reset visited nodes
        netlist.reset()

    return current_path, current_cost