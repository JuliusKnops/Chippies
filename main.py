import csv

class Netlist():
    def __init__(self, netlist_sourcefile, print_sourcefile):
        self.gates = self.load_gates(print_sourcefile)
        self.load_connections(netlist_sourcefile)

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
        self.x = x_coordinate
        self.y = y_coordinate
        self.name = name  
        self.connections = set()
    
    def add_connections(self, NewPoint):
        self.connections.add(NewPoint)

if __name__ == "__main__":
    chip_nr = 0 # loopt van 0 tot en met 2
    netlist_nr = 1 # loopt van 1 tot en met 3

    netlist_file = f"data/chip_{chip_nr}/netlist_{netlist_nr + 3 * chip_nr}.csv"
    print_file = f"data/chip_{chip_nr}/print_{chip_nr}.csv"
    
    netlist = Netlist(netlist_file, print_file)

    print(netlist.gates)

    for chip in netlist.gates:
        print(chip, netlist.gates[chip].x, netlist.gates[chip].y, netlist.gates[chip].connections)
    