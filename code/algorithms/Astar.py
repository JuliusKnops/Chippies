import heapq
import main

class Node:
    def __init__(self, x, y, z, cost = 0, parent = None):
        self.x = x
        self.y = y
        self.z = z
        self.cost = cost
        self.parent = parent

    # NOTE: This is code for a different project that still needs to be
    #       converted. This code assumes that each point is incremently numbered
    #       for example a 7x7 grid is numbered from 0 to 48.
    # TODO: Convert code to fit this project's needs
    def next_moves(self):
       # check if up and down possible
        rest = int(pos_index % self.map_rows)
        if rest == 0:
            pos_index_up = pos_index
            pos_index_down = pos_index + 1
        elif rest == (self.map_rows-1):
            pos_index_up = pos_index - 1
            pos_index_down = pos_index
        else:
            pos_index_up = pos_index - 1
            pos_index_down = pos_index + 1

        # check if left and right possible
        division = float((pos_index+1)) / float(self.map_rows)
        if division > (self.map_columns - 1):
            pos_index_left = pos_index
            pos_index_right = pos_index - self.map_rows
        elif division <= 1:
            pos_index_left = pos_index + self.map_rows
            pos_index_right = pos_index
        else:
            pos_index_left = pos_index + self.map_rows
            pos_index_right = pos_index - self.map_rows

        # set has no index, so change it
        # NOTE: made it a set
        return tuple(set((pos_index, pos_index_up, pos_index_down, pos_index_left, pos_index_right)))

    # Allows qheap to auto sort
    def __lt__(self, other):
        global destination_node
        self_estimate = ( (self.x - destination_node.x)**2 + 
                          (self.y - destination_node.y)**2 +
                          (self.z - destination_node.z)**2
                            ) **.5
        other_estimate = ( (other.x - destination_node.x)**2 + 
                           (other.y - destination_node.y)**2 +
                           (other.z - destination_node.z)**2
                            ) **.5

        return (self.cost + self_estimate) < (other.cost + other_estimate)

    # This functions checks if goal state is reached.
    # NOTE: without this function, eq seems to fail even when the cost and parent attribute match...?
    def __eq__(self, other):
        if self.x == other.x and self.y == other.y and self.z == other.z:
            return True
        return False

# [ [(2, 4, 4), (4, 2, 4), (3, 4, 5), (3, 4, 3)], [(2, 4, 4), (4, 2, 4)] ]

class PathFinder(object):

    def __init__(self, Start_chip, End_chip, auto_pathfind = True):
        self.Start_chip = Start_chip
        self.End_chip = End_chip

        if auto_pathfind:
            self.path = self.astar()

    #######################
    ### Unfinished Astar
    #######################
    # NOTE: possibly increment cost issues. Right now the cost always starts at
    #       1, but it should start at 0. However, does it even matter if all 
    #       start at 1? It shouldn't affect the final result.
    def astar(self):
        from main import grid_rows, grid_cols, grid_layers
        # NOTE __lt__ needs to know the goal node
        global destination_node
        start = self.Start_chip
        destination_node = self.End_chip

        # Temporary remove destination_node from gates so we are only checking
        # for other gates that are not the start or end.
        main.Astar_netlist.gate_locations.remove( (destination_node.x, destination_node.y, destination_node.z) )

        # print(main.Astar_netlist.used_connections)
        heap = []

        # push start node into the heap
        heapq.heappush(heap, (0, start))

        visited = set()

        # while there are still nodes to check...
        while heap:
            # return node with smallest cost from the heap stack
            current = heapq.heappop(heap)[1]
            
            # checks if goal node
            if current == destination_node:
                path = []
                # returns the path and then reverse the order
                # NOTE: order start at the end and ends at the start.
                #       We visit each parent node until no parent node
                #       left, e.g. we reached the start.
                while current:
                    node = (current.x, current.y, current.z)
                    path.append(node)
                    current = current.parent

                    # Don't add node if gate node
                    # NOTE: search in list is O(n), should be fast
                    if node in main.Astar_netlist.gate_locations:
                        continue
                    # Intersection if node already in use and not a gate
                    # NOTE: search in list is O(n), should be fast
                    if node in main.Astar_netlist.used_nodes:
                        main.Astar_netlist.k += 1
                    # NOTE 1: also saves gates location. Might be an issue.
                    # NOTE 2: Wastes memory by double saving
                    # EDIT: Fixed by if statement 
                    main.Astar_netlist.used_nodes.add(node)

                # Re-add gate
                main.Astar_netlist.gate_locations.add( (destination_node.x, destination_node.y, destination_node.z) )

                return path[::-1]

            # skip Node if already visited
            if (current.x, current.y, current.z) in visited:
                continue
            visited.add((current.x, current.y, current.z))

            ######################
            ### bug fixing
            ######################
            # self_estimate = ( (current.x - destination_node.x)**2 + 
            #               (current.y - destination_node.y)**2 +
            #               (current.z - destination_node.z)**2
            #                 ) **.5
            # cost_est = self_estimate + current.cost
            # print(current.x, current.y, current.z, " cost + estimation: ", cost_est)
            ######################
            ### end of bug fixing
            ######################

            # Moves, checks if move is not out of bounds, then adds new Node
            # to heap with its parent Node.
            # NOTE: is another way for the next_move func. Total possibilities are
            # 3! = 6.
            for dx, dy, dz in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]:
                x, y, z = current.x + dx, current.y + dy, current.z + dz
                if not (0 <= x < grid_rows and 0 <= y < grid_cols and 0 <= z < grid_layers):
                    continue
                
                # INVALID NODE IF GATE NODE
                if (x, y, z) in main.Astar_netlist.gate_locations:
                    continue
                
                # skip if connection already occupied
                nodes_connection = { (current.x, current.y, current.z), (x, y, z) }
                if nodes_connection in main.Astar_netlist.used_connections:
                    continue

                cost = current.cost + 1
                # TODO; make non spaghetti code. If check is double.
                # NOTE: gates will never be added to used_nodes set
                if (x, y, z) in main.Astar_netlist.used_nodes:
                    # increament by 300 due to short circuit
                    cost += 300 

                # extend heap with new node
                heapq.heappush(heap, (cost, Node(x, y, z, cost, current)))

        # Re-add gate before raising exception
        main.Astar_netlist.gate_locations.add( (destination_node.x, destination_node.y, destination_node.z) )

        # NOTE: If there is no valid pad raise exception for easier bugfixing.
        #       Else it returns None.
        raise Exception("Failed to find a path.")

# all_connections structure: [ (start_node, end_node), (start_node, end_node)...]
def find_all_paths(all_connections, as_objects = False):
    # from main import Astar_netlist
    all_paths = []
    
    for connection in all_connections:
        start_node, end_node = connection
        path = PathFinder(start_node, end_node)
        all_paths.append(path)

        # add connections to used_connections
        for i in range( (len(path.path)-1) ):
            wire = frozenset({path.path[i], path.path[i+1]})
            # print(wire, " ",type(wire))
            main.Astar_netlist.used_connections.add(wire)
            main.Astar_netlist.n += 1
    print(main.Astar_netlist.n, main.Astar_netlist.k)
    # if {(1, 0, 0), (0, 0, 0)} in Astar_netlist.used_connections:
    #     print("True")
    # if {(0, 0, 0), (1, 0, 0)} in Astar_netlist.used_connections:
    #     print("True")
    # print(Astar_netlist.used_connections)
    # print(main.Astar_netlist.used_connections)


    if as_objects:
        return all_paths

    return [pf.path for pf in all_paths]

if __name__ == '__main__':
    grid_rows = 3
    grid_cols = 3
    grid_layers = 1
    # 2x2 grid with only 1 layer
    grid = [
            [ # start of layer
            [[0, 0, 0], [0, 1, 0]], # X-axis row 1 
            [[1, 0, 0], [1, 1, 0]]  # X-axis row 2
                 ] # end of layer
                ]
    start = Node(0, 0, 0)
    end = Node(2, 2, 0)

    # astar_example = PathFinder(start, end)
    # print(astar_example.path)

    chip_nr = 0 # loopt van 0 tot en met 2
    netlist_nr = 1 # loopt van 1 tot en met 3

    netlist_file = f"data/chip_{chip_nr}/netlist_{netlist_nr + 3 * chip_nr}.csv"
    print_file = f"data/chip_{chip_nr}/print_{chip_nr}.csv"

    Astar_netlist = Netlist(netlist_file, print_file)

    print(find_all_paths([ (start, end) ]))