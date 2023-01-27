
"""
In plaats van controleren of een move gaat naar een node die al bezet is, (1, 2) in visited,
kijken of tweetal van nodes als paar in visited zit ((xn1, yn1), (xn2, yn2)) en ((xn2, yn2), (xn1, yn1)) zo kijken of dit segment al
gelopen is.
"""
from code.classes.netlist import *
from code.classes.gates import *
import random

def random_algo(netlist):

    # create set for visited nodes on grid
    visited = set()

    # create list for end solution
    solution = []

    # get invalid nodes of placed gates on grid
    invalid_nodes = netlist.invalid_gates #get_invalid_nodes(netlist)
    
    # for each gate in netlist
    for gates in netlist.get_gates():

        # create start_gate and get coordinates of object
        start_gate = gates.get_coordinates() #(gates.x, gates.y, gates.z)

        # for each connection of the starting_gate
        for connection in gates.connections:

            # create end_gate variable and get coordinates of object
            end_gate = connection.get_coordinates() #(connection.x, connection.y, connection.z)

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

                # reset the possible move list, happens when starting for a new point or when the whole path gets resetted
                possible_moves = reset_possible_moves(reset, possible_moves)

                # pick random move from possible moves
                random_move = random.choice(possible_moves)
               
                # calculate new position of wire's end by adding random move to current wire position
                new_wire_location = calculate_wire_pos(new_wire_location, random_move, '+') 

                # check if new position is a valid position 
                # (check if node has not been visited before, node is not another gate and node is not out of bounds)
                if not valid_node(new_wire_location, visited, invalid_nodes, path, netlist):
                    
                    # remove made move from list of possible moves
                    possible_moves.remove(random_move)

                    # reverse the made move and return to previous position
                    new_wire_location = calculate_wire_pos(new_wire_location, random_move, '-') 
                    
                    # next iteration the list will not return to standard list
                    reset = False

                    # if all possible moves are removed from a possition, reset the current path and start over from start_gate
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
    
    return solution
    

def reset_possible_moves(reset, possible_moves):
    if reset:
        return [(1,0,0), (0,1,0), (-1,0,0), (0,-1,0), (0,0,1), (0,0,-1)]
    return possible_moves

def path_reset(path, new_wire_location, hard_stuck, possible_moves, start_gate):
    if len(possible_moves) == 0:
        reset = True
        path = [start_gate]
        new_wire_location = start_gate
        hard_stuck += 1
        return path, new_wire_location, reset, hard_stuck
    return path, new_wire_location, False, hard_stuck

def calculate_wire_pos(new_wire_location, random_move, dir):
    if dir == '+':
        return (new_wire_location[0] + random_move[0], new_wire_location[1] + random_move[1], new_wire_location[2] + random_move[2])
    return (new_wire_location[0] - random_move[0], new_wire_location[1] - random_move[1], new_wire_location[2] - random_move[2])

def add_to_path(new_wire_location, path):
    if new_wire_location not in path:   
        path.append(new_wire_location) 
        reset = True
        return path, reset
    return path, False

def check_goal(new_wire_location, path, end_gate):
    if (new_wire_location[0] - end_gate[0], new_wire_location[1] - end_gate[1], new_wire_location[2] - end_gate[2]) in [(1,0,0), (0,1,0), (-1,0,0), (0,-1,0), (0,0,1), (0,0,-1)]:
        #path.append(new_wire_location)
        path.append(end_gate)
        found_path = True 
        return path, found_path
    return path, False

# functies aanpassen naar class functies -> class variables aanmaken voor visited en path, zodat aantal parameters naar netlist en location gaan.
def out_of_bounds(current_node, netlist):
    return not (0 <= current_node[0] <= netlist.get_max_x() and 0 <= current_node[1] <= netlist.get_max_y() and 0 <= current_node[2] <= netlist.get_max_z())
# functies aanpassen naar class functies -> class variables aanmaken voor visited en path, zodat aantal parameters naar netlist en location gaan.
def valid_node(current_node, visited, invalid_nodes, path, netlist):
    return (not (current_node in visited or current_node in invalid_nodes or current_node in path)) and not out_of_bounds(current_node, netlist)

def update_visited(visited, path):
    for nodes in path:
        visited.add(nodes)
    return visited

def update_solution(solution, path):
    tmp_solution = []
    for nodes in path:
        tmp_solution.append(nodes)
    solution.append(tmp_solution)
    return solution

def check_hard_stuck(hard_stuck):
    if hard_stuck == 100:
        return True

# call this function to create a random solution. In case of hardstuck None gets returned initially.
# this function makes in case of hardstuck to be sure to reset / recall function and try again  
def get_randomize_solution(netlist):
    found_solution = random_algo(netlist)
    while not found_solution:
       found_solution = random_algo(netlist)
    return found_solution
