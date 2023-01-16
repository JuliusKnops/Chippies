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