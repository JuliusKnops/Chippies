"""
Random_Algorithm.py

Chippies
Julius Knops, Deniz Mermer, Hidde Brenninkmeijer
Algoritmen & Heuristieken

A random algorithm that connects gates with a given netlist
"""

from code.classes.netlist import *
from code.classes.gates import *
import random

from typing import Tuple, TypeVar

import time

NetlistObject = TypeVar("NetlistObject")

def random_algo(netlist: NetlistObject):
    """
    Returns a random solution for given gates and netlist
    """

    # create set for visited nodes / edges on grid
    visited = set()

    # create list for end solution
    solution = []

    # get invalid nodes of placed gates on grid
    invalid_nodes = netlist.invalid_gates_list 
    
    # for each gate in netlist
    for gates in netlist.get_gates():

        # create start_gate and get coordinates of object
        start_gate = gates.get_coordinates() 

        # for each connection of the starting_gate
        for connection in gates.connections:

            # create end_gate variable and get coordinates of object
            end_gate = connection.get_coordinates() 
            
            # create list for path between start gate and end gate, starting with start_gate
            path = [start_gate]
        
            # start location of wire starts at the start_gate location
            new_wire_location = start_gate

            found_path = False
            reset = True
            
            # start with all possible moves
            possible_moves = [(1,0,0), (0,1,0), (0,0,1), (-1,0,0), (0,-1,0), (0,0,-1)]

            # variable for reset the whole netlist, incase of complete stuckness or too many moves from point A to point B
            hard_stuck = 0
            n_moves = 0

            # while start_gate and end_gate are not connected
            while not found_path:
                
                # check if current path is in a hardstuck position
                if check_hard_stuck(hard_stuck, n_moves):
                    return

                # reset the possible move list, happens when starting from a new point or when current path gets resetted
                possible_moves = reset_possible_moves(reset, possible_moves)

                # pick random move from possible moves
                random_move = random.choice(possible_moves)
               
                # calculate new position of wire's end by adding random move to current wire position
                current_wire_location = new_wire_location
                new_wire_location = calculate_wire_pos(current_wire_location, random_move) 

                # used_unit is the edge between Node 1 and Node 2, noted as ((N1X, N1Y, N1Z), (N2X, N2Y, N2Z))
                used_unit = check_edge_connection(current_wire_location, new_wire_location)

                # check if new position is a valid position 
                # (check if node has not been visited before, node is not another gate and node is not out of bounds)
                if not valid_node(used_unit, visited, invalid_nodes, netlist, start_gate, end_gate):
                    
                    # remove made move from list of possible moves
                    possible_moves.remove(random_move)

                    # reverse the made move and return to previous position
                    new_wire_location = current_wire_location
                    
                    # next iteration the possible_moves list will not return to standard form
                    # previous made moves cannot occur
                    reset = False

                    # if all possible moves are removed from a possition, reset the current path and start over from start_gate
                    # then increase hard stuck by one
                    path, new_wire_location, reset, hard_stuck = path_reset(path, new_wire_location, hard_stuck, possible_moves, start_gate)
                
                # new node is valid
                else:
                    # increase current number of made moves between start and end gate
                    n_moves += 1

                    # update path list with the new connection
                    path, reset = add_to_path(new_wire_location, path)

                    # if new current location is 1 valid move removed from end point, make that move
                    path, found_path = check_goal(new_wire_location, path, end_gate, visited)

            # update current visited with found path
            visited = update_visited(visited, path)

            # update current solution with found path
            solution = update_solution(solution, path)

    # save current solution
    netlist.set_solution(solution)
    return netlist.calculate_cost(), solution
    

def reset_possible_moves(reset: bool, possible_moves: list) -> list:
    """
    When a valid move has been made, the list with possible moves gets resetted to
    standard form, with all possible moves 
    """
    if reset:
        return [(1,0,0), (0,1,0), (-1,0,0), (0,-1,0), (0,0,1), (0,0,-1)]
    return possible_moves

def path_reset(path: list, new_wire_location: tuple, 
               hard_stuck: int, possible_moves: list, 
               start_gate: tuple) -> Tuple[list, tuple, bool, int]:
    """
    When the number of possible moves from any point equals 0, the current path gets resetted
    hardstuck gets increased by 1
    """
    if len(possible_moves) == 0:
        reset = True
        path = [start_gate]
        new_wire_location = start_gate
        hard_stuck += 1
        return path, new_wire_location, reset, hard_stuck
    return path, new_wire_location, False, hard_stuck

def calculate_wire_pos(current_wire_location: tuple, random_move: tuple) -> tuple:
    """
    Returns Tuple of new position of the wire by adding dx, dy, dz to current position
    """
    return (current_wire_location[0] + random_move[0], 
            current_wire_location[1] + random_move[1], 
            current_wire_location[2] + random_move[2])
    
def add_to_path(new_wire_location: tuple, path: list) -> Tuple[list, bool]: 
    """
    New location gets added to the path
    """  
    path.append(new_wire_location) 
    reset = True

    # Incase a path makes a crossing in its own path, the points visited between the crossing get removed. 
    # Remove loop in own path
    seen = set()
    dupes = [d for d in path if d in seen or seen.add(d)]
    
    for d in dupes:
        path = path[:path.index(d) + 1]

    return path, reset
    

def check_goal(new_wire_location: tuple, path: list, 
               end_gate: tuple, visited: set) -> Tuple[list, bool]:
    """
    When wire is 1 valid move removed from end gate, make that connection
    """
    dx = new_wire_location[0] - end_gate[0]
    dy = new_wire_location[1] - end_gate[1]
    dz = new_wire_location[2] - end_gate[2]

    if (dx, dy, dz) in [(1,0,0), (0,1,0), (0,0,1), (-1,0,0), (0,-1,0), (0,0,-1)] and \
        not check_edge_connection(new_wire_location, end_gate) in visited:
        
        path.append(end_gate)
        found_path = True 
        return path, found_path

    return path, False


def out_of_bounds(edge_connection: tuple, netlist: NetlistObject) -> bool:
    """
    Checks if a move is out of bounds
    """
    for node in edge_connection:
        if not (0 <= node[0] <= netlist.get_max_x() and 
                0 <= node[1] <= netlist.get_max_y() and 
                0 <= node[2] <= netlist.get_max_z()):
            return True
    return False
   

def valid_node(edge_connection: tuple, visited: set, invalid_nodes: set, 
               netlist: NetlistObject, start_gate: tuple, end_gate: tuple) -> bool:
    """
    Checks if new move is valid
    """

    # if edge_connection has been visited in prior moves, move is invalid
    # no overlap of wires 
    if edge_connection in visited:
        return False
    
    # check if new point is located in dimension of chip
    if out_of_bounds(edge_connection, netlist):
        return False

    # check if a node of edge_connection is not a different gate
    for node in edge_connection:
        if (node in invalid_nodes and (node != start_gate and node != end_gate)):
            return False

    return True

def update_visited(visited: set, path: list) -> set:
    """
    visited is a set that consist of Tuples indicating edge connections
    after a path has been made, the edge connections get added to the set
    """
    for nodes in range(len(path) - 1):
        visited.add(check_edge_connection(path[nodes], path[nodes + 1]))
    return visited

def update_solution(solution: list, path: list) -> list:
    tmp_solution = []
    for nodes in path:
        tmp_solution.append(nodes)
    solution.append(tmp_solution)
    return solution

def check_hard_stuck(hard_stuck: int, n_moves: int) -> bool:
    """
    if current attempt of creating a path leads to N hard stucks or takes M total moves
    the current attempt is marked as hard stuck.
    """
    if hard_stuck == 100 or n_moves == 10000:
        return True
    return False


def check_edge_connection(current: tuple, new: tuple) -> tuple:
    """
    https://www.geeksforgeeks.org/python-sort-list-of-tuple-based-on-sum/
    edge connections are as follow: ((x1, y1, z1), (x2, y2, z2))
    the order of Tuples in Tuple is determined by the sum of each x, y, z values
    Tuple with the lowest sum is placed on index 0
    """
    lst = [current, new]

    for i in range(len(lst)):
        for j in range(len(lst) - i - 1):
            if (lst[j][0]+lst[j][1]+lst[j][2]) > (lst[j+1][0]+lst[j+1][1]+lst[j+1][2]):
                lst[j], lst[j+1], lst[1] = lst[1], lst[j+1], lst[j]
    return tuple(lst)


def get_randomize_solution(netlist: NetlistObject) -> tuple:
    """
    call this function to create a random solution. In case of hardstuck None gets returned initially.
    this function makes in case of hardstuck to be sure to reset / recall function and try again  
    """

    found_solution = random_algo(netlist)
    while not found_solution:
        found_solution = random_algo(netlist)

    return found_solution


        