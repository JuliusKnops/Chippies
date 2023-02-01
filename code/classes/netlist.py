import csv 
import config
import random
import more_itertools as mit

from .gates import Gates

class Netlist():
    def __init__(self, netlist_sourcefile: str, print_sourcefile: str):

        if config.random_netlist:
            self.gates = self.get_random_gates()
            self.get_random_connections()
        else:
            self.gates = self.load_gates(print_sourcefile)
            self.load_connections(netlist_sourcefile)

        self.invalid_gates_list = self.invalid_gates()
        self.dimension = self.get_dimensions()

        self.solution = []

        #########################################################
        ### Insert gate locations, connections, nodes and n, k cost
        #########################################################
        self.used_connections = set()
        self.used_nodes = set()
        self.gate_locations = set([(int(g.x), int(g.y), g.z) for \
                                        g in self.gates.values()])

        self.k = 0
        self.n = 0

        self.connection_tuples = self.get_connection_tuples()
        
        ###############################
        ### End
        ###############################


    # reads the print.csv file and creates the gate objects with 
    # given coordinates
    def load_gates(self, sourcefile: str) -> dict:
        gates = {}

        with open(sourcefile) as in_file:
            reader = csv.DictReader(in_file) 

            for row in reader:
                gate = list(row.values())
                gate_name = gate[0]
                gate_x = gate[1]
                gate_y = gate[2]
                gate_z = 0 if len(gate) == 3 else gate[3]
                gates[gate_name] = Gates(gate_name, gate_x, gate_y, gate_z)

        return gates
    
    # reads the netlist.csv file and add to each gate the given connections
    def load_connections(self, sourcefile: str):
        with open(sourcefile) as in_file:
            reader = csv.DictReader(in_file)
            for row in reader:
                connections = list(row.values())
                gate_a = connections[0]
                gate_b = connections[1]
                self.gates[gate_a].add_connections(self.gates[gate_b])

    def get_random_gates(self) -> dict:
        """
        Generates random gates. Number of gates based on config settings.
        """
        gates = set()

        # randomly generate gates until max reached
        while len(gates) < config.gates_max:
            x = random.randint(0, config.x_max)
            y = random.randint(0, config.y_max)

            gate_nr = len(gates)
            gate = Gates( gate_nr, x, y, 0 )

            gates.add( gate )

        # return dic for consistency
        return { gate.name:gate for gate in gates }

    def get_random_connections(self):
        """
        Creates random connections based on existing gates.
        The number of connections is based on config settings.
        """
        connections = set()

        # create list of gates
        gate_objects = [self.gates[gate_nr] for gate_nr in self.gates]
        
        # randomly assign connections until max reached
        while len(connections) < config.connections_max:
            # get a random connection out of all possible connections
            connection = mit.random_permutation(gate_objects, 2)

            # make frozenset in order to add to a set and avoid dupes
            connection = frozenset(connection)
            connections.add(connection)

        # add gates connections to gate objects
        for connection in connections:
            gate1, gate2 = connection
            self.gates[gate1.name].add_connections(gate2)
    
    # returns a set with invalid nodes.
    # if a gate is located on a node with a z > 0, than every node
    # below the gate is also considered as invalid
    def invalid_gates(self) -> set:
        invalid_nodes = set()
        for gate in self.gates.values():
            for z in range(gate.z + 1):
                invalid_nodes.add((gate.x, gate.y, z))
        return invalid_nodes

    def get_connection_tuples(self) -> list:
        connection_set = set()
        for chip in self.gates:
            current_x_loc = self.gates[chip].x
            current_y_loc = self.gates[chip].y
            current_z_loc = self.gates[chip].z
            current_loc = (current_x_loc, current_y_loc, current_z_loc)
            start_loc = current_loc
            for connections in self.gates[chip].connections:
                end_loc = (connections.x, connections.y, connections.z)
                connection = frozenset((start_loc, end_loc))
                connection_set.add(connection)
        
        return [ tuple(c) for c in connection_set ]
    
    # returns all gate objects that are in the current netlist dictionary
    def get_gates(self) -> list:
        return self.gates.values()

    # calculates the minimum dimension of the chip.
    def get_dimensions(self) -> tuple:
    # dimensies ook mogelijk als parameter invoeren wanneer netlist class 
    # aangemaakt word
    # standaard x, y en z op 0 zetten, tenzij die als parameters worden meegeven
        x_max = 0
        y_max = 0
        z_max = 7

        x_min = 0
        y_min = 0
        z_min = 0
        for gate in self.gates.values():
            x_max = gate.x if gate.x > x_max else x_max
            y_max = gate.y if gate.y > y_max else y_max
            #z_max = gate.z if gate.z > z_max else z_max
            x_min = gate.x if gate.x < x_min else x_min
            y_min = gate.y if gate.y < y_min else y_min
            #z_min = gate.z if gate.z < z_min else z_min
        return (x_min - 1, y_min - 1, z_min), (x_max + 1, y_max + 1, z_max)
    
    def get_max_x(self):
        return self.dimension[1][0]

    def get_max_y(self):
        return self.dimension[1][1]

    def get_max_z(self):
        return self.dimension[1][2]
    
    def get_min_x(self):
        return self.dimension[0][0]

    def get_min_y(self):
        return self.dimension[0][1]

    def get_min_z(self):
        return self.dimension[0][2]
    
    def set_solution(self, solution):
        self.solution = solution

    def count_crossings(self) -> int:
        crossing = []
        for path in self.solution:
            path = path[1:len(path) - 1]
            for node in path:
                crossing.append(node)
        
        return len(crossing) - len(set(crossing))

    def is_valid(self) -> bool:
        valid = []
        for path in self.solution:
            for node in range(len(path) - 1):
                valid.append((path[node], path[node + 1]))

        return len(valid) == len(set(valid))    
    
    def calculate_cost(self) -> int:
        return self.count_units() + 300 * self.count_crossings()

    def fitness(self) -> int:
        try:
            return abs(1/self.calculate_cost())
        except:
            return 0
    
    def count_units(self) -> int:
        units = 0
        for path in self.solution:
            units += len(path) - 1
        return units

    def reset(self):
        self.used_nodes = set()
        self.used_connections = set()
        self.n = 0
        self.k = 0
        self.gate_locations = set([(int(g.x), int(g.y), g.z) for \
                                        g in self.gates.values()])
