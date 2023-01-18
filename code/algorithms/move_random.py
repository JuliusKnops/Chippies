"""import random
def move_random(netlist):
    print("functie is aangeroepen")
    x_max = 7
    y_max = 7
    z_max = 7
    n = 0
    k = 0
    made_moves = set()
    max_dim_xyz = (x_max, y_max, z_max)
    #netlist = {1: chip1, 2:chip2}
    
    Manhatten probleem toepassen, niet direct terug kunnen gaan

    for chip in netlist.gates:
        print(f"for chip-loop: {chip}")
        for connections in netlist.gates[chip].connections:
            print(f"connections = {connections}")
            print(f"netlist.gates[chip].x = {netlist.gates[chip].x}")
            current_x_loc = netlist.gates[chip].x
            current_y_loc = netlist.gates[chip].y
            current_z_loc = netlist.gates[chip].z
            prev_move = None
            new_move = None
            possible_moves = [(1,0,0), (0,1,0), (0,0,1), (-1,0,0),(0,-1,0), (0,0,-1)]

            current_loc = (current_x_loc, current_y_loc, current_z_loc)
            end_loc = (connections.x, connections.y, connections.z)

            while current_loc !=  end_loc:

                while True:
                    if len(possible_moves) == 0:
                        break

                    new_move = random.choice(possible_moves)
                    new_loc = (current_loc[0] + new_move[0], current_loc[1] + new_move[1], current_loc[2] + new_move[2])

                    if new_loc in made_moves or not (0 < new_loc[0] < max_dim_xyz[0] and 0 < new_loc[1] < max_dim_xyz[1] and 0 < new_loc[2] < max_dim_xyz[2]):
                        possible_moves.remove(new_move)
                    else:
                        made_moves.append(new_loc)
                        current_loc = new_loc
                        n += 1
    return n

if 0 <= new_loc[0] <= x_max and 0 <= new_loc[1] <= y_max and 0 <= new_loc[2] <= z_max:
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

def move_random(netlist):
    print("functie is aangeroepen")
    x_max = 7
    y_max = 7
    z_max = 7
    n = 0
    k = 0
    made_moves = set()
    max_dim_xyz = (x_max, y_max, z_max)
    #netlist = {1: chip1, 2:chip2}
    
    Manhatten probleem toepassen, niet direct terug kunnen gaan

    for chip in netlist.gates:
        current_x_loc = netlist.gates[chip].x
        current_y_loc = netlist.gates[chip].y
        current_z_loc = netlist.gates[chip].z

        start_loc = (current_x_loc, current_y_loc, current_z_loc)


        for connections in netlist.gates[chip].connections:
            
            possible_moves = [(1,0,0), (0,1,0), (0,0,1), (-1,0,0),(0,-1,0), (0,0,-1)]

            current_loc = (current_x_loc, current_y_loc, current_z_loc)
            end_loc = (connections.x, connections.y, connections.z)

            while current_loc !=  end_loc:

                while True:
                    if len(possible_moves) == 0:
                        break

                    new_move = random.choice(possible_moves)
                    new_loc = (current_loc[0] + new_move[0], current_loc[1] + new_move[1], current_loc[2] + new_move[2])

                    if new_loc in made_moves or not (0 < new_loc[0] < max_dim_xyz[0] and 0 < new_loc[1] < max_dim_xyz[1] and 0 < new_loc[2] < max_dim_xyz[2]):
                        possible_moves.remove(new_move)
                    else:
                        made_moves.append(new_loc)
                        current_loc = new_loc
                        n += 1
    return n"""


def random_algo(netlist):

    visited = set()
    

    for gates in netlist.gates.values():

        start_location = (gates.x, gates.y, gates.z)
        wire_location = start_location

        for connection in gates.connections:

            end_location = (connection.x, connection.y, connection.z)

            while start_location != end_location:
                pass

def find_path(pointA, pointB):
    pass
