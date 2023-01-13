import csv 

class Netlist():
    def __init__(self, netlist_sourcefile, print_sourcefile):
        self.gates = self.load_gates(print_sourcefile)
        #self.load_connections(print_sourcefile)
        print(self.gates)

    def load_gates(self, sourcefile):
        gates = {}

        with open(sourcefile) as in_file:
            reader = csv.DictReader(in_file) 

            for row in reader:
                chip_name = row['chip']
                chip_x = row['x']
                chip_y = row['y']
                #print(chip_name, chip_x, chip_y)
                gates[row['chip']] = Gates(chip_x, chip_y)
        return gates

class Gates():
    def __init__(self, x_coordinate, y_coordinate):
        self.x = x_coordinate
        self.y = y_coordinate


if __name__ == "__main__":
    chip_nr = 0 # loopt van 0 tot en met 2
    netlist_nr = 1 # loopt van 1 tot en met 3

    netlist_file = f"Python-files/GatesAndNetlists/chip_{chip_nr}/netlist_{netlist_nr + 3 * chip_nr}.csv"
    print_file = f"Python-files/GatesAndNetlists/chip_{chip_nr}/print_{chip_nr}.csv"
    
    graphs = Netlist(netlist_file, print_file)

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
