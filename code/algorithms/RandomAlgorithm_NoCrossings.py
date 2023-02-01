"""
RandomAlgorithm_NoCrossings.py

Chippies
Julius Knops, Deniz Mermer, Hidde Brenninkmeijer
Algoritmen & Heuristieken

A random algorithm that connects gates with a given netlist
Moves are made randomly, however moves cannot overlap with each other
and crossings are not allowed
"""

from code.classes.netlist import *
from code.classes.gates import *
import random
from typing import TypeVar

NetlistObject = TypeVar("NetlistObject")

def Start_Random_Algorithm(netlist: NetlistObject) -> tuple:

    # create set for visited nodes on grid
    visited = set()

    # create list for end solution
    solution = []

    # get invalid nodes of placed gates on grid
    invalid_nodes = netlist.invalid_gates #get_invalid_nodes(netlist)
    
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

            # variable for reset the whole netlist, incase of complete stuckness
            hard_stuck = 0

            # while start_gate and end_gate are not connected
            while not found_path:

                # check if current completion is not forming a hardstuck for next gate
                if check_hard_stuck(hard_stuck):
                    return

                # reset the possible move list, happens when starting 
                # for a new point or when the whole path gets resetted
                possible_moves = reset_possible_moves(reset, possible_moves)

                # pick random move from possible moves
                random_move = random.choice(possible_moves)
               
                # calculate new position of wire's end by adding 
                # random move to current wire position
                new_wire_location = calculate_wire_pos(new_wire_location, random_move, '+') 

                # check if new position is a valid position 
                # (check if node has not been visited before, 
                # node is not another gate and node is not out of bounds)
                if not valid_node(new_wire_location, visited, invalid_nodes, path, netlist):
                    
                    # remove made move from list of possible moves
                    possible_moves.remove(random_move)

                    # reverse the made move and return to previous position
                    new_wire_location = calculate_wire_pos(new_wire_location, random_move, '-') 
                    
                    # next iteration the list will not return to standard list
                    reset = False

                    # if all possible moves are removed from a possition, 
                    # reset the current path and start over from start_gate
                    # then increase hard stuck by one
                    path, new_wire_location, reset, hard_stuck = path_reset(path, new_wire_location, hard_stuck, possible_moves, start_gate)
                
                # new node is valid
                else:
                    # update path list with the new connection
                    path, reset = add_to_path(new_wire_location, path)

                    # if new current location is 1 move removed from end point, make that move
                    path, found_path = check_goal(new_wire_location, path, end_gate)
                
            visited = update_visited(visited, path)
            solution = update_solution(solution, path)
    
    netlist.set_solution(solution)
    return netlist.calculate_cost(), solution, netlist.invalid_gates_list
    
def reset_possible_moves(reset: bool, possible_moves: list) -> list:
    """
    When a valid move has been made, the list with possible moves gets resetted
    to standard form, with all possible moves 
    """
    if reset:
        return [(1,0,0), (0,1,0), (-1,0,0), (0,-1,0), (0,0,1), (0,0,-1)]
    return possible_moves

def path_reset(path: list, new_wire_location: tuple, 
                hard_stuck: int, possible_moves: list, start_gate: tuple) -> tuple:
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

def calculate_wire_pos(new_wire_location: tuple, 
                        random_move: tuple, dir: str) -> tuple:
    """
    Returns Tuple of new position of the wire by adding dx, dy, dz to current position
    """
    if dir == '+':
        return (new_wire_location[0] + random_move[0], 
                new_wire_location[1] + random_move[1], 
                new_wire_location[2] + random_move[2])
    return (new_wire_location[0] - random_move[0], 
            new_wire_location[1] - random_move[1], 
            new_wire_location[2] - random_move[2])

def add_to_path(new_wire_location: tuple, path: list) -> tuple:
    """
    New location gets added to the path
    """  
    if new_wire_location not in path:   
        path.append(new_wire_location) 
        reset = True
        return path, reset
    return path, False

def check_goal(new_wire_location: tuple, path: list, end_gate: tuple) -> tuple:
    """
    When wire is 1 valid move removed from end gate, make that connection
    """
    dx = new_wire_location[0] - end_gate[0]
    dy = new_wire_location[1] - end_gate[1]
    dz = new_wire_location[2] - end_gate[2]

    if (dx, dy, dz) in [(1,0,0), (0,1,0), (0,0,1), (-1,0,0), (0,-1,0), (0,0,-1)]:
        
        path.append(end_gate)
        found_path = True 
        return path, found_path

    return path, False

def out_of_bounds(current_node: tuple, netlist: NetlistObject) -> bool:
    """
    Checks if a move is out of bounds
    """
    return not (0 <= current_node[0] <= netlist.get_max_x() and 
                0 <= current_node[1] <= netlist.get_max_y() and 
                0 <= current_node[2] <= netlist.get_max_z())

def valid_node(current_node: tuple, visited: set, invalid_nodes: set, path: list, netlist: NetlistObject) -> bool:
    """
    Checks if new move is valid
    """
    return (not (current_node in visited or 
                current_node in invalid_nodes or 
                current_node in path)) and \
                not out_of_bounds(current_node, netlist)

def update_visited(visited: set, path: list) -> set:
    """
    visited is a set that consist of Tuples indicating edge connections
    after a path has been made, the edge connections get added to the set
    """
    for nodes in path:
        visited.add(nodes)
    return visited

def update_solution(solution: list, path: list) -> list:
    """
    When a new path has been made, add new path to current solution list
    """
    tmp_solution = []
    for nodes in path:
        tmp_solution.append(nodes)
    solution.append(tmp_solution)
    return solution

def check_hard_stuck(hard_stuck: int) -> bool:
    """
    if current attempt of creating a path leads to N hard stucks or 
    takes M total moves the current attempt is marked as hard stuck.
    """
    if hard_stuck == 100:
        return True
 
def get_randomize_solution(netlist: NetlistObject) -> tuple:
    """
    call this function to create a random solution. 
    In case of hardstuck None gets returned initially.
    this function makes in case of hardstuck to be sure to reset function
    """
    found_solution = Start_Random_Algorithm(netlist)
    while not found_solution:
       found_solution = Start_Random_Algorithm(netlist)
    return found_solution



