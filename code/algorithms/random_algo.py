
"""
In plaats van controleren of een move gaat naar een node die al bezet is, (1, 2) in visited,
kijken of tweetal van nodes als paar in visited zit ((xn1, yn1), (xn2, yn2)) en ((xn2, yn2), (xn1, yn1)) zo kijken of dit segment al
gelopen is.
"""
from code.classes.netlist import *
from code.classes.gates import *
import random
# import csv

# class Netlist():
#     def __init__(self, netlist_sourcefile, print_sourcefile):
#         self.gates = self.load_gates(print_sourcefile)
#         self.load_connections(netlist_sourcefile)
#         self.invalid_gates = self.invalid_gates()
#         self.dimension = self.get_dimensions()

#         self.solution = []

#         #########################################################
#         ### Insert gate locations, connections, nodes and n, k cost
#         #########################################################
#         self.used_connections = set()
#         self.used_nodes = set()
#         self.gate_locations = set([(int(g.x), int(g.y), g.z) for g in self.gates.values()])

#         self.k = 0
#         self.n = 0

#         ###############################
#         ### End
#         ###############################


#         #####
#         # Toevoegen van berekende functies zoals kosten, aantal units en valid als boolean.
#         # functie aanroepen en dit opslaan onder class attribute
#         #####

#     # reads the print.csv file and creates the gate objects with given coordinates
#     def load_gates(self, sourcefile):
#         gates = {}

#         with open(sourcefile) as in_file:
#             reader = csv.DictReader(in_file) 

#             for row in reader:
#                 gate = list(row.values())
#                 gate_name = gate[0]
#                 gate_x = gate[1]
#                 gate_y = gate[2]
#                 gate_z = 0 if len(gate) == 3 else gate[3]
#                 gates[gate_name] = Gates(gate_name, gate_x, gate_y, gate_z)

#         return gates
    
#     # reads the netlist.csv file and add to each gate the given connections
#     def load_connections(self, sourcefile):
#         with open(sourcefile) as in_file:
#             reader = csv.DictReader(in_file) 
#             for row in reader:
#                 connections = list(row.values())
#                 gate_a = connections[0]
#                 gate_b = connections[1]
#                 self.gates[gate_a].add_connections(self.gates[gate_b])
    
#     # returns a set with invalid nodes.
#     # if a gate is located on a node with a z > 0, than every node
#     # below the gate is also considered as invalid
#     def invalid_gates(self):
#         invalid_nodes = set()
#         for gate in self.gates.values():
#             for z in range(gate.z):
#                 invalid_nodes.add((gate.x, gate.y, z))
#         return invalid_nodes
    
#     # returns all gate objects that are in the current netlist dictionary
#     def get_gates(self):
#         return self.gates.values()

#     # calculates the minimum dimension of the chip.
#     def get_dimensions(self):
#     # dimensies ook mogelijk als parameter invoeren wanneer netlist class aangemaakt word
#     # standaard x, y en z op 0 zetten, tenzij die als parameters worden meegeven
#         x_max = 0
#         y_max = 0
#         z_max = 7

#         x_min = 0
#         y_min = 0
#         z_min = 0
#         for gate in self.gates.values():
#             x_max = gate.x if gate.x > x_max else x_max
#             y_max = gate.y if gate.y > y_max else y_max
#             #z_max = gate.z if gate.z > z_max else z_max
#             x_min = gate.x if gate.x < x_min else x_min
#             y_min = gate.y if gate.y < y_min else y_min
#             #z_min = gate.z if gate.z < z_min else z_min
#         return (x_min - 1, y_min - 1, z_min), (x_max + 1, y_max + 1, z_max)
    
#     def get_max_x(self):
#         return self.dimension[1][0]

#     def get_max_y(self):
#         return self.dimension[1][1]

#     def get_max_z(self):
#         return self.dimension[1][2]
    
#     def get_min_x(self):
#         return self.dimension[0][0]

#     def get_min_y(self):
#         return self.dimension[0][1]

#     def get_min_z(self):
#         return self.dimension[0][2]
    
#     def set_solution(self, solution):
#         self.solution.append(solution)

#     # self.solution is de huidige oplossing van het pad met begin gates en eind gates erin
#     # dit kan ook vervangen worden voor een lijst waarin deze niet standaard in zitten, dus
#     # dan is het gelijk len(self.solution) - len(set(self.solution)) kunnen returnen
#     def count_crossings(self):
#         crossing = []
#         for path in self.solution:
#             path = path[1:len(path) - 1]
#             for node in path:
#                 crossing.append(node)
        
#         return len(crossing) - len(set(crossing))

#     def is_valid(self):
#         valid = []
#         for path in self.solution:
#             for node in range(len(path) - 1):
#                 valid.append((path[node], path[node + 1]))

#         return len(valid) == len(set(valid))    
    
#     def calculate_cost(self):
#         return self.count_units() + 300 * self.count_crossings()

#     def fitness(self):
#         try:
#             return abs(1/self.calculate_cost())
#         except:
#             return 0
    
#     def count_units(self):
#         units = 0
#         for path in self.solution:
#             units += len(path) - 1
#         return units

# class Gates():
#     def __init__(self, name, x_coordinate, y_coordinate, z_coordinate):
#         self.x = int(x_coordinate)
#         self.y = int(y_coordinate)
#         self.z = int(z_coordinate)
#         self.name = name  
#         self.connections = set()
    
#     def add_connections(self, NewPoint):
#         self.connections.add(NewPoint)
    
#     def get_coordinates(self):
#         return (self.x, self.y, self.z)


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

# if __name__ == "__main__":
#     chip_nr = 0 # loopt van 0 tot en met 2
#     netlist_nr = 1 # loopt van 1 tot en met 3

#     netlist_file = f"../../data/chip_{chip_nr}/netlist_{netlist_nr + 3 * chip_nr}.csv"
#     print_file = f"../../data/chip_{chip_nr}/print_{chip_nr}.csv"
    
#     netlist = Netlist(netlist_file, print_file)

#     #print(f"netlist.gates = {netlist.gates}")

#     #for chip in netlist.gates:
#     #    print(chip, netlist.gates[chip].x, netlist.gates[chip].y, netlist.gates[chip].connections)
    
#     #move_random(netlist)
#     #print(random_algo(netlist))

#     random_paths = []
#     random_paths = random_algo(netlist)
#     while not random_paths:
#        random_paths = random_algo(netlist)
    
#     print(random_paths)

"""
[[(1, 5, 0), (1, 4, 0), (2, 4, 0), (2, 4, 1), (2, 5, 1), (2, 5, 2), (2, 4, 2), (3, 4, 2), (3, 4, 1), (4, 4, 1), (4, 4, 0)], [(1, 5, 0), (0, 5, 0), (0, 6, 0), (0, 6, 1), (1, 6, 1), (1, 6, 2), (1, 7, 2), (1, 7, 1), (1, 8, 1), (1, 8, 0), (1, 7, 0), (2, 7, 0), (2, 6, 0), (2, 5, 0), (3, 5, 0), (3, 4, 0), (3, 3, 0), (3, 2, 0), (3, 2, 1), (4, 2, 1), (4, 3, 1), (5, 3, 1), (6, 3, 1), (6, 3, 0), (6, 4, 0), (6, 5, 0)], [(4, 4, 0), (5, 4, 0), (5, 5, 0), (5, 5, 1), (5, 4, 1), (6, 4, 1), (6, 4, 2), (7, 4, 2), (7, 3, 2), (8, 3, 2), (8, 3, 3), (8, 2, 3), (8, 1, 3), (8, 1, 4), (9, 1, 4), (9, 1, 5), (9, 0, 5), (8, 0, 5), (7, 0, 5), (6, 0, 5), (6, 0, 6), (5, 0, 6), (5, 0, 5), (5, 1, 5), (5, 2, 5), (6, 2, 5), (7, 2, 5), (7, 1, 5), (7, 1, 4), (7, 1, 3), (6, 1, 3), (6, 1, 2), (6, 1, 1), (6, 0, 1), (5, 0, 1), (5, 1, 1), (5, 2, 1), (5, 2, 2), (5, 1, 2), (5, 0, 2), (4, 0, 2), (4, 0, 1), (3, 0, 1), (3, 0, 0), (3, 1, 0)], [(6, 2, 0), (6, 2, 1), (7, 2, 1), (7, 2, 0), (7, 3, 0), (7, 4, 0), (7, 5, 0), (6, 5, 0)], [(6, 2, 0), (6, 1, 0), (6, 0, 0), (5, 0, 0), (5, 1, 0), (5, 2, 0), (5, 3, 0), (4, 3, 0), (4, 2, 0), (4, 1, 0), (3, 1, 0)]]
"""