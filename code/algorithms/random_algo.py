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

    print("FUNCTIE AANGEROEPEN")

    visited = set()
    solution = []

    invalid_nodes = set()
    for gate in netlist.gates.values():
        invalid_nodes.add((gate.x, gate.y, gate.z)) # class attribute van maken in netlist
    print(f"invalid nodes = {invalid_nodes}")

    for gates in netlist.gates.values():

        start_gate = (gates.x, gates.y, gates.z)

        print(f"start gate = {gates.name} op locatie {start_gate}")

        wire_location = start_gate

        for connection in gates.connections:

            end_gate = (connection.x, connection.y, connection.z)
            print(f"end gate = {connection.name} op locatie {end_gate}")

            path = []
            path.append(start_gate)
            print(path)

            new_wire_location = start_gate

            # loop
            found_path = False
            reset = True
            while not found_path:

                if reset:
                    possible_moves = [(1,0,0), (0,1,0), (-1,0,0), (0,-1,0), (0,0,1), (0,0,-1)]

                random_move = random.choice(possible_moves)

                new_wire_location = (new_wire_location[0] + random_move[0], new_wire_location[1] + random_move[1], new_wire_location[2] + random_move[2])

                if (new_wire_location[0] - end_gate[0], new_wire_location[1] - end_gate[1], new_wire_location[2] - end_gate[2]) in [(1,0,0), (0,1,0), (-1,0,0), (0,-1,0), (0,0,1), (0,0,-1)]:
                    path.append(new_wire_location)
                    path.append(end_gate)
                    found_path = True 
                    print("PAD GEVONDEN")
                    break
                
                if not valid_node(new_wire_location, visited, invalid_nodes, path):
                    print("NOT VALID")
                    possible_moves.remove(random_move)
                    reset = False
                    new_wire_location = (new_wire_location[0] - random_move[0], new_wire_location[1] - random_move[1], new_wire_location[2] - random_move[2])
                
                    if len(possible_moves) == 0:
                        reset = True
                        path = []
                        new_wire_location = (start_gate[0], start_gate[1], start_gate[2])

                if new_wire_location not in path:   
                    path.append(new_wire_location) 
                    reset = True
            
            tmp_solution = []
            for x in path:
                #print(f"x = {x}")
                visited.add(x)
                tmp_solution.append(x)
            solution.append(tmp_solution)
    return solution

def find_path(start_gate, end_gate):
    """
    path en visited gescheiden houden, path pas toevoegen aan visited wanneer het een valid path is.
    anders worden de punten bij visited gelijk toegevoegd, ook wanneer er een reset plaats vind en de vorige
    paden verwijderd worden.

    als distance tussen wire en end_gate 1 is (manhatten distance), dan connecten aan punt
    i.p.v. dat de lijn vlak voor gate nog naar boven kan gaan etc.
    """



    path = []
    path.append(start_gate)

    new_wire_location = start_gate

    # loop
    found_path = False
    reset = True
    while not found_path:

        if reset:
            possible_moves = [(1,0,0), (0,1,0), (-1,0,0), (0,-1,0), (0,0,1), (0,0,-1)]

        random_move = random.choice(possible_moves)

        new_wire_location = (new_wire_location[0] + random_move[0], new_wire_location[1] + random_move[1], new_wire_location[2] + random_move[2])

        if (new_wire_location[0] - end_gate[0], new_wire_location[1] - end_gate[1], new_wire_location[2] - end_gate[2]) in [(1,0,0), (0,1,0), (-1,0,0), (0,-1,0), (0,0,1), (0,0,-1)]:
            path.append(new_wire_location)
            path.append(end_gate)
            found_path = True 
            break
        
        if not valid_node(new_wire_location):
            possible_moves.remove(random_move)
            reset = False
            new_wire_location = (new_wire_location[0] - random_move[0], new_wire_location[1] - random_move[1], new_wire_location[2] - random_move[2])
        
            if len(possible_moves) == 0:
                reset = True
                path = []
                new_wire_location = (start_gate[0], start_gate[1], start_gate[2])

        if new_wire_location not in path:   
            path.append(new_wire_location) 
            reset = True


def out_of_bounds(location):
    return not (0 <= location[0] <= 7 and 0 <= location[1] <= 7 and 0 <= location[2] <= 7)

def valid_node(location, visited, invalid_nodes, path):
    return not (location in visited or location in invalid_nodes or location in path) and not out_of_bounds(location)

    

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