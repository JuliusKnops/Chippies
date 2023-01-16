import csv
import random

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
        self.x = int(x_coordinate)
        self.y = int(y_coordinate)
        self.z = 0
        self.name = name  
        self.connections = set()
    
    def add_connections(self, NewPoint):
        self.connections.add(NewPoint)

# seed kiezen voor 
def move_random(netlist):
    print("functie is aangeroepen")
    x_max = 7
    y_max = 7
    z_max = 7
    n = 0
    k = 0
    made_moves = set()
    #netlist = {1: chip1, 2:chip2}
    
    """ Manhatten probleem toepassen, niet direct terug kunnen gaan"""

    for chip in netlist.gates:
        print(f"for chip-loop: {chip}")
        for connections in netlist.gates[chip].connections:
            print(f"connections = {connections}")
            inbounds = True
            print(f"netlist.gates[chip].x = {netlist.gates[chip].x}")
            while netlist.gates[chip].x != connections.x or netlist.gates[chip].y != connections.y or netlist.gates[chip].z != connections.z:
                print(f"while loop")
                # kies willekeurige richting, x-, y-, of z-as
                move_axis = random.choice(['x', 'y', 'z']) #([netlist.gates[chip].x, netlist.gates[chip].y, netlist.gates[chip].z])
                move_direction = random.choice([-1, 1])
                # willekeurige richting op gekozen as gaan
                if move_axis == 'x':
                    netlist.gates[chip].x += move_direction
                elif move_axis == 'y':
                    netlist.gates[chip].y += move_direction
                elif move_axis == 'z':
                    netlist.gates[chip].z += move_direction

                """print(f"move axis = {move_axis}")
                # kies willekeurige richting in bovengekozen as
                move_direction = random.choice([-1, 1])
                print(f"move direction = {move_direction}")
                move_axis += move_direction"""
                # inbounds?
                if 0 <= netlist.gates[chip].x <= x_max and 0 <= netlist.gates[chip].y <= y_max and 0 <= netlist.gates[chip].z <= z_max:
                    if (netlist.gates[chip].x, netlist.gates[chip].y, netlist.gates[chip].z) in made_moves: 
                        k += 1
                        print(f"k = {k}")
                    made_moves.add((netlist.gates[chip].x, netlist.gates[chip].y, netlist.gates[chip].z))
                    n += 1
                    print(f"n = {n}")
                else:
                    if move_axis == 'x':
                        netlist.gates[chip].x -= move_direction
                    elif move_axis == 'y':
                        netlist.gates[chip].y -= move_direction
                    elif move_axis == 'z':
                        netlist.gates[chip].z -= move_direction

if __name__ == "__main__":
    chip_nr = 0 # loopt van 0 tot en met 2
    netlist_nr = 1 # loopt van 1 tot en met 3

    netlist_file = f"data/chip_{chip_nr}/netlist_{netlist_nr + 3 * chip_nr}.csv"
    print_file = f"data/chip_{chip_nr}/print_{chip_nr}.csv"
    
    netlist = Netlist(netlist_file, print_file)

    print(f"netlist.gates = {netlist.gates}")

    for chip in netlist.gates:
        print(chip, netlist.gates[chip].x, netlist.gates[chip].y, netlist.gates[chip].connections)
    
    move_random(netlist)
    
