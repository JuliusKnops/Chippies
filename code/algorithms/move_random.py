import random
import time

# seed kiezen voor 
def move_random(netlist):
    print("functie is aangeroepen")
    x_max = 8
    y_max = 8
    z_max = 0
    n = 0
    k = 0
    made_moves = set()
    max_dim_xyz = (x_max, y_max, z_max)
    #netlist = {1: chip1, 2:chip2}
    invalid_nodes = set()
    for chip in netlist.gates:
        invalid_nodes.add((netlist.gates[chip].x, netlist.gates[chip].y)) # class attribute van maken in netlist

    #invalid_nodes = [(netlist.gates.x, netlist.gates.y) for (netlist.gates.x, netlist.gates.y) in netlist.gates]
    #print(invalid_nodes)
    #quit()
    
    """ Manhatten probleem toepassen, niet direct terug kunnen gaan"""

    for chip in netlist.gates:
        print(f"for chip-loop: {chip}")
        current_x_loc = netlist.gates[chip].x
        current_y_loc = netlist.gates[chip].y
        current_z_loc = netlist.gates[chip].z
        current_loc = (current_x_loc, current_y_loc, current_z_loc)
        start_loc = current_loc
        for connections in netlist.gates[chip].connections:
            print(f"connections = {connections}")
            print(f"netlist.gates[chip].x = {netlist.gates[chip].x}")
            end_loc = (connections.x, connections.y, connections.z)
            possible_moves = [(1,0,0), (0,1,0),  (-1,0,0),(0,-1,0)] # (0,0,1), , (0,0,-1)
            while current_loc != end_loc and len(possible_moves) != 0:
                print(f"current_loc = {current_loc}, end_loc = {end_loc}")
                #possible_moves = [(1,0,0), (0,1,0), (-1,0,0),(0,-1,0)]
                #print(len(possible_moves))
                #while len(possible_moves) != 0 and current_loc !=  end_loc:

                new_move = random.choice(possible_moves)
                new_loc = (current_loc[0] + new_move[0], current_loc[1] + new_move[1], current_loc[2] + new_move[2])
                print(f"new_loc = {new_loc}")
                if new_loc in made_moves or new_loc in invalid_nodes or not (0 <= new_loc[0] <= max_dim_xyz[0] and 0 <= new_loc[1] <= max_dim_xyz[1] and 0 <= new_loc[2] <= max_dim_xyz[2]):
                    print(f"REMOVE MOVE: in made moves = {new_loc in made_moves}")
                    possible_moves.remove(new_move)

                    if len(possible_moves) == 0:
                        possible_moves = [(1,0,0), (0,1,0), (-1,0,0),(0,-1,0)]
                        current_loc = (current_x_loc, current_y_loc, current_z_loc)
                        print("RESET")
                        time.sleep(0.5)
                        made_moves = set()
                else:
                    print("MOVE GEVONDEN< TOEVOEGEN")
                    made_moves.add(current_loc)
                    current_loc = new_loc
                    n += 1
                    possible_moves = [(1,0,0), (0,1,0), (-1,0,0),(0,-1,0)]
        print(f"PAD GEVONDEN: Made moves {start_loc} {end_loc}: {made_moves} {len(made_moves)}")
        time.sleep(5.5)

    return n

def greedy(netlist):
    total_distance = 0

    invalid_nodes = set()
    for chip in netlist.gates:
        invalid_nodes.add((netlist.gates[chip].x, netlist.gates[chip].y))

    for start_gate in netlist.gates.values():
        for end_gate in start_gate.connections:
            # Create a queue to store the next cells to visit
            print(f"start gate = {start_gate.name} | end gate = {end_gate.name}")
            queue = [(start_gate.x, start_gate.y, 0)]
            # Create a set to store visited cells
            visited = set()
            # Define the possible moves for the algorithm
            moves = [[1, 0], [-1, 0], [0, 1], [0, -1]]
            
            while queue:
                # Get the first cell from the queue
                x, y, dist = queue.pop(0)
                # If the cell is the end_gate, return the distance
                if x == end_gate.x and y == end_gate.y:
                    total_distance += dist
                    print(f"dist = {dist}")
                    break
                # If the cell has been visited, continue to the next cell
                if (x, y) in visited or ((x, y) in invalid_nodes and (x, y) != (start_gate.x, start_gate.y)):
                    continue
                # Mark the cell as visited
                visited.add((x, y))
                # Add all valid, unvisited moves to the queue
                for dx, dy in moves:
                    if 0 <= x+dx <= 20 and 0 <= y+dy <= 20:
                        #if grid[x+dx][y+dy] != "#":
                        queue.append((x+dx, y+dy, dist+1))
            # If the end_gate is not reached, return -1
            return -1
    return total_distance, visited