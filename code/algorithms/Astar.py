import heapq
import config

class Node_Astar:
    def __init__(self, x, y, z, cost = 0, parent = None):
        self.x = x
        self.y = y
        self.z = z
        self.cost = cost
        self.parent = parent

    # Allows qheap to auto sort
    def __lt__(self, other):
        """
        Allows qheap to auto sort. Finding the most promising using heuristics.
        """
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

class PathFinder_Astar(object):

    def __init__(self, Start_chip, End_chip, auto_pathfind = True, Node = Node_Astar):
        self.Start_chip = Start_chip
        self.End_chip = End_chip

        if auto_pathfind:
            self.path, self.cost = self.astar(Node = Node)

    def astar(self, Node = Node_Astar):
        """
        If Astar node, calculates most promising node using heuristics.
        Else, uses dijkstra. Astar can be converted to dijkstra if the used
        heuristic for estimation is always 0.
        """
        grid_rows = config.Astar_netlist.dimension[0]
        grid_cols = config.Astar_netlist.dimension[1]
        grid_layers = config.Astar_netlist.dimension[2] - 1

        # split grid layers in up and down
        grid_layers_up = int(grid_layers / 2)
        grid_layers_down = -grid_layers_up

        # NOTE: __lt__ needs to know the goal node
        global destination_node
        start = self.Start_chip
        destination_node = self.End_chip

        # Temporary remove destination_node from gates so we are only checking
        # for other gates that are not the start or end.
        config.Astar_netlist.gate_locations.remove( (destination_node.x, destination_node.y, destination_node.z) )

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
                # save final cost before pathing back to start
                cost = current.cost

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
                    if node in config.Astar_netlist.gate_locations:
                        continue
                    # Intersection if node already in use and not a gate
                    # NOTE: search in list is O(n), should be fast
                    if node in config.Astar_netlist.used_nodes:
                        config.Astar_netlist.k += 1
                
                    config.Astar_netlist.used_nodes.add(node)

                # Re-add gate
                config.Astar_netlist.gate_locations.add( (destination_node.x, destination_node.y, destination_node.z) )

                # remove used node as gate
                config.Astar_netlist.used_nodes.remove( (destination_node.x, destination_node.y, destination_node.z) )

                return path[::-1], cost

            # skip Node if already visited
            if (current.x, current.y, current.z) in visited:
                continue
            visited.add((current.x, current.y, current.z))

            # Moves, checks if move is not out of bounds, then adds new Node
            # to heap with its parent Node.
            # NOTE: is another way for the next_move func. Total possibilities
            #       are 3! = 6.
            for dx, dy, dz in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]:
                x, y, z = current.x + dx, current.y + dy, current.z + dz
                if not (0 <= x < grid_rows and 0 <= y < grid_cols):
                    continue
                
                if not grid_layers_down <= z <= grid_layers_up:
                    continue
                                
                # INVALID NODE IF GATE NODE
                if (x, y, z) in config.Astar_netlist.gate_locations:
                    continue
                
                # skip if connection already occupied
                nodes_connection = { (current.x, current.y, current.z), (x, y, z) }
                if nodes_connection in config.Astar_netlist.used_connections:
                    continue

                cost = current.cost + 1
                
                # NOTE: gates will never be added to used_nodes set
                if (x, y, z) in config.Astar_netlist.used_nodes:
                    # increament by 300 due to short circuit
                    cost += 300 

                # extend heap with new node
                heapq.heappush(heap, (cost, Node(x, y, z, cost, current)))

        # Re-add gate before raising exception
        config.Astar_netlist.gate_locations.add( (destination_node.x, destination_node.y, destination_node.z) )

        # NOTE: If there is no valid pad raise exception for easier bugfixing.
        #       Else it returns None.
        raise Exception("Failed to find a path.")


# if __name__ == '__main__':
#     grid_rows = 3
#     grid_cols = 3
#     grid_layers = 1
#     # 2x2 grid with only 1 layer
#     grid = [
#             [ # start of layer
#             [[0, 0, 0], [0, 1, 0]], # X-axis row 1 
#             [[1, 0, 0], [1, 1, 0]]  # X-axis row 2
#                  ] # end of layer
#                 ]
#     start = Node(0, 0, 0)
#     end = Node(2, 2, 0)

#     # astar_example = PathFinder(start, end)
#     # print(astar_example.path)

#     chip_nr = 0 # loopt van 0 tot en met 2
#     netlist_nr = 1 # loopt van 1 tot en met 3

#     netlist_file = f"data/chip_{chip_nr}/netlist_{netlist_nr + 3 * chip_nr}.csv"
#     print_file = f"data/chip_{chip_nr}/print_{chip_nr}.csv"

#     Astar_netlist = Netlist(netlist_file, print_file)

#     print(find_all_paths([ (start, end) ]))