import csv 
from .gates import *

class Netlist():
    def __init__(self, netlist_sourcefile, print_sourcefile):
        self.gates = self.load_gates(print_sourcefile)
        self.load_connections(netlist_sourcefile)
        self.invalid_gates = self.invalid_gates()
        self.dimension = self.get_dimensions()

        self.solution = None

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


        #####
        # Toevoegen van berekende functies zoals kosten, aantal units en valid als boolean.
        # functie aanroepen en dit opslaan onder class attribute
        #####

    def load_gates(self, sourcefile):
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
    
    def load_connections(self, sourcefile):
        with open(sourcefile) as in_file:
            reader = csv.DictReader(in_file) 
            for row in reader:
                connections = list(row.values())
                gate_a = connections[0]
                gate_b = connections[1]
                self.gates[gate_a].add_connections(self.gates[gate_b])
    
    def invalid_gates(self):
        invalid_nodes = set()
        for gate in self.gates.values():
            for z in range(gate.z):
                invalid_nodes.add((gate.x, gate.y, z))
        return invalid_nodes
    
    # dimensies ook mogelijk als parameter invoeren wanneer netlist class aangemaakt word
    # standaard x, y en z op 0 zetten, tenzij die als parameters worden meegeven
    def get_dimensions(self):
        x_max = 0
        y_max = 0
        z_max = 7
        for gate in self.gates.values():
            x_max = gate.x if gate.x > x_max else x_max
            y_max = gate.y if gate.y > y_max else y_max
            #z_max = gate.z if gate.z > z_max else z_max
        return (x_max + 1, y_max + 1, z_max)
    
    def get_x(self):
        return self.dimension[0]

    def get_y(self):
        return self.dimension[1]

    def get_z(self):
        return self.dimension[2]
    
    def set_solution(self, solution):
        self.solution = solution

    # self.solution is de huidige oplossing van het pad met begin gates en eind gates erin
    # dit kan ook vervangen worden voor een lijst waarin deze niet standaard in zitten, dus
    # dan is het gelijk len(self.solution) - len(set(self.solution)) kunnen returnen
    def count_crossings(self):
        crossing = []
        for path in self.solution:
            path = path[1:len(path) - 1]
            for node in path:
                crossing.append(node)
        
        return len(crossing) - len(set(crossing))

    def is_valid(self):
        valid = []
        for path in self.solution:
            for node in range(len(path) - 1):
                valid.append((path[node], path[node + 1]))

        return len(valid) == len(set(valid))    
    
    def calculate_cost(self):
        return self.count_units() + 300 * self.count_crossings()

    def fitness(self):
        try:
            return abs(1/self.calculate_cost())
        except:
            return 0
    
    def count_units(self):
        units = 0
        for path in self.solution:
            units += len(path) - 1
        return units
