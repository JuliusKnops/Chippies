import csv
import random
#from code.algorithms.Astar import *
import time

class Netlist():
    def __init__(self, netlist_sourcefile, print_sourcefile):
        self.gates = self.load_gates(print_sourcefile)
        self.load_connections(netlist_sourcefile)

        #########################################################
        ### Insert gate locations, connections, nodes and n, k cost
        #########################################################
        self.used_connections = set()
        self.used_nodes = set()
        self.gate_locations = set([(int(g.x), int(g.y), g.z) for g in self.gates.values()])

        self.k = 0
        self.n = 0

        ###############################
        ### End
        ###############################

    def load_gates(self, sourcefile):
        gates = {}

        with open(sourcefile) as in_file:
            reader = csv.DictReader(in_file) 

            for row in reader:
                gates[row['chip']] = Gates(row['x'], row['y'], row['chip'])

        return gates
    
    def load_connections(self, sourcefile):
        with open(sourcefile) as in_file:
            reader = csv.DictReader(in_file) 
            for row in reader:
                self.gates[row['chip_a']].add_connections(self.gates[row['chip_b']])

class Gates():
    def __init__(self, x_coordinate, y_coordinate, name):
        self.x = int(x_coordinate)
        self.y = int(y_coordinate)
        self.z = 0
        self.name = name  
        self.connections = set()
    
    def add_connections(self, NewPoint):
        self.connections.add(NewPoint)

def random_algo(netlist):

    # create set for visited nodes on grid
    visited = set()

    # create list for end solution
    solution = []

    # get invalid nodes of placed gates on grid
    invalid_nodes = get_invalid_nodes(netlist)

    # for each gate in netlist
    for gates in netlist.gates.values():

        # create start_gate and get coord
        start_gate = (gates.x, gates.y, gates.z)

        # for each connection of the starting_gate
        for connection in gates.connections:

            # create end_gate variable
            end_gate = (connection.x, connection.y, connection.z)
            #print(f"end gate = {connection.name} op locatie {end_gate}")

            # create empty list for path between start gate and end gate
            path = []

            # add starting gate to path
            path.append(start_gate)
        
            # start location of wire starts at the start_gate location
            new_wire_location = start_gate

            found_path = False
            reset = True
            
            # start with all possible moves
            possible_moves = [(1,0,0), (0,1,0), (-1,0,0), (0,-1,0), (0,0,1), (0,0,-1)]

            # while start_gate and end_gate are not connected
            while not found_path:

                # reset the possible move list, happens when starting for a new point or when the whole path gets resetted
                possible_moves = reset_possible_moves(reset, possible_moves)

                # pick random move from possible moves
                random_move = random.choice(possible_moves)
               
                # calculate new position of wire's end by adding random move to current wire position
                new_wire_location = calculate_wire_pos(new_wire_location, random_move, '+') 

                # check if new position is a valid position 
                # (check if node has not been visited before, node is not another gate and node is not out of bounds)
                if not valid_node(new_wire_location, visited, invalid_nodes, path):
                    
                    # remove made move from list of possible moves
                    possible_moves.remove(random_move)

                    # reverse the made move and return to previous position
                    new_wire_location = calculate_wire_pos(new_wire_location, random_move, '-') 
                    
                    # next iteration the list will not return to standard list
                    reset = False

                    # if all possible moves are removed from a possition, reset the current path and start over from start_gate
                    path, new_wire_location, reset = path_reset(possible_moves, start_gate, new_wire_location, path)
                
                # new node is valid
                else:
                    # update path list with the new connection
                    path, reset = add_to_path(new_wire_location, path)

                    # if new current location is 1 move removed from end point, make that move
                    path, found_path = check_goal(new_wire_location, path, end_gate)
                
            visited = update_visited(visited, path)
            solution = update_solution(solution, path)

    return solution

def get_invalid_nodes(netlist):
    invalid_nodes = set()
    for gate in netlist.gates.values():
        invalid_nodes.add((gate.x, gate.y, gate.z)) # class attribute van maken in netlist
    print(f"invalid nodes = {invalid_nodes}")
    return invalid_nodes

def reset_possible_moves(reset, possible_moves):
    if reset:
        return [(1,0,0), (0,1,0), (-1,0,0), (0,-1,0), (0,0,1), (0,0,-1)]
    return possible_moves

def path_reset(possible_moves, start_gate, new_wire_location, path):
    if len(possible_moves) == 0:
        reset = True
        path = [start_gate]
        new_wire_location = start_gate
        return path, new_wire_location, reset
    return path, new_wire_location, False

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
        path.append(new_wire_location)
        path.append(end_gate)
        found_path = True 
        return path, found_path
    return path, False

def out_of_bounds(location):
    return not (0 <= location[0] <= 7 and 0 <= location[1] <= 7 and 0 <= location[2] <= 7)

def valid_node(location, visited, invalid_nodes, path):
    return (not (location in visited or location in invalid_nodes or location in path)) and not out_of_bounds(location)

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


if __name__ == "__main__":
    chip_nr = 0 # loopt van 0 tot en met 2
    netlist_nr = 1 # loopt van 1 tot en met 3

    netlist_file = f"../../data/chip_{chip_nr}/netlist_{netlist_nr + 3 * chip_nr}.csv"
    print_file = f"../../data/chip_{chip_nr}/print_{chip_nr}.csv"
    
    netlist = Netlist(netlist_file, print_file)

    #print(f"netlist.gates = {netlist.gates}")

    #for chip in netlist.gates:
    #    print(chip, netlist.gates[chip].x, netlist.gates[chip].y, netlist.gates[chip].connections)
    
    #move_random(netlist)
    print(random_algo(netlist))

"""
[[(1, 5, 0), (1, 4, 0), (2, 4, 0), (2, 4, 1), (2, 5, 1), (2, 5, 2), (2, 4, 2), (3, 4, 2), (3, 4, 1), (4, 4, 1), (4, 4, 0)], [(1, 5, 0), (0, 5, 0), (0, 6, 0), (0, 6, 1), (1, 6, 1), (1, 6, 2), (1, 7, 2), (1, 7, 1), (1, 8, 1), (1, 8, 0), (1, 7, 0), (2, 7, 0), (2, 6, 0), (2, 5, 0), (3, 5, 0), (3, 4, 0), (3, 3, 0), (3, 2, 0), (3, 2, 1), (4, 2, 1), (4, 3, 1), (5, 3, 1), (6, 3, 1), (6, 3, 0), (6, 4, 0), (6, 5, 0)], [(4, 4, 0), (5, 4, 0), (5, 5, 0), (5, 5, 1), (5, 4, 1), (6, 4, 1), (6, 4, 2), (7, 4, 2), (7, 3, 2), (8, 3, 2), (8, 3, 3), (8, 2, 3), (8, 1, 3), (8, 1, 4), (9, 1, 4), (9, 1, 5), (9, 0, 5), (8, 0, 5), (7, 0, 5), (6, 0, 5), (6, 0, 6), (5, 0, 6), (5, 0, 5), (5, 1, 5), (5, 2, 5), (6, 2, 5), (7, 2, 5), (7, 1, 5), (7, 1, 4), (7, 1, 3), (6, 1, 3), (6, 1, 2), (6, 1, 1), (6, 0, 1), (5, 0, 1), (5, 1, 1), (5, 2, 1), (5, 2, 2), (5, 1, 2), (5, 0, 2), (4, 0, 2), (4, 0, 1), (3, 0, 1), (3, 0, 0), (3, 1, 0)], [(6, 2, 0), (6, 2, 1), (7, 2, 1), (7, 2, 0), (7, 3, 0), (7, 4, 0), (7, 5, 0), (6, 5, 0)], [(6, 2, 0), (6, 1, 0), (6, 0, 0), (5, 0, 0), (5, 1, 0), (5, 2, 0), (5, 3, 0), (4, 3, 0), (4, 2, 0), (4, 1, 0), (3, 1, 0)]]
"""