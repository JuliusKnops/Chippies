import csv

class Netlist():
    def __init__(self, netlist_sourcefile, print_sourcefile):
        self.gates = self.load_gates(print_sourcefile)
        self.load_connections(netlist_sourcefile)
        #print(self.gates)

    def load_gates(self, sourcefile):
        gates = {}

        with open(sourcefile) as in_file:
            reader = csv.DictReader(in_file) 

            for row in reader:
                chip_name = row['chip']
                chip_x = row['x']
                chip_y = row['y']
                #print(chip_name, chip_x, chip_y)
                gates[row['chip']] = Gates(chip_x, chip_y, chip_name)
        return gates
    
    def load_connections(self, sourcefile):
        with open(sourcefile) as in_file:
            reader = csv.DictReader(in_file) 
            for row in reader:
                print(f"row = {row}")
                print(self.gates)
                print(f"row chip_a = {row['chip_a']}")
                print(self.gates[row['chip_a']])
                self.gates[row['chip_a']].add_connections(self.gates[row['chip_b']])  
                ##if row[1] == str(l):
                 #   print("ja")
            """for row in reader:
                print(f"row = {row}")
                for l in self.gates:
                    print(l)"""


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

    netlist_file = f"Python-files/GatesAndNetlists/chip_{chip_nr}/netlist_{netlist_nr + 3 * chip_nr}.csv"
    print_file = f"Python-files/GatesAndNetlists/chip_{chip_nr}/print_{chip_nr}.csv"
    
    netlist = Netlist(netlist_file, print_file)

    print(netlist.gates)

    for chip in netlist.gates:
        print(chip, netlist.gates[chip].x, netlist.gates[chip].y, netlist.gates[chip].connections)
    



"""    with open(netlist_file) as in_file:
        reader = csv.DictReader(in_file) 

        for row in reader:
            print(row)
    
    with open(print_file) as in_file:
        reader = csv.DictReader(in_file) 

        for row in reader:
            chip_name = row['chip']
            chip_x = row['x']
            chip_y = row['y']
            print(chip_name, chip_x, chip_y)"""
    


"""
import csv
def load_nodes(self, source_file):
    nodes = {}

    with open(self, source_file) as in_file:
        reader = csv.csv.DictReader(in_file) 

        for row in reader:
"""
