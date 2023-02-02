import heapq
import config

class Node_Astar:
    def __init__(self, x: int, y: int, z: int, cost = 0, parent = None) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.cost = cost
        self.parent = parent

    # Allows qheap to auto sort
    def __lt__(self, other):
        """
        Allows qheap to auto sort. Finding the most promising using heuristics.
        The function is f(x) = h(x) + g(x) 
        with h(x) the current cost en g(x) the estimation
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

    def __eq__(self, other):
        """
        This functions checks if goal state is reached.
        """
        if self.x == other.x and self.y == other.y and self.z == other.z:
            return True
        return False

class PathFinder_Astar(object):

    def __init__(self, Start_chip: object, End_chip: object, 
                auto_pathfind = True, 
                Node = Node_Astar) -> None:
        self.Start_chip = Start_chip
        self.End_chip = End_chip

        if auto_pathfind:
            self.path, self.cost = self.astar(Node = Node)

    def astar(self, Node = Node_Astar) -> tuple:
        """
        If Astar node, calculates most promising node using heuristics.
        Else, uses dijkstra. Astar can be converted to dijkstra if the used
        heuristic for estimation is always 0.
        """
        grid_rows = config.Astar_netlist.dimension[1][0] + 1
        grid_cols = config.Astar_netlist.dimension[1][1] + 1
        grid_layers = config.Astar_netlist.dimension[1][2]

        # NOTE: __lt__ needs to know the goal node
        global destination_node
        start = self.Start_chip
        destination_node = self.End_chip

        # Temporary remove destination_node from gates so we are only checking
        # for other gates that are not the start or end.
        config.Astar_netlist.gate_locations.remove((destination_node.x, 
                                                    destination_node.y,
                                                    destination_node.z))

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
                config.Astar_netlist.gate_locations.add((   destination_node.x,
                                                            destination_node.y,
                                                            destination_node.z))

                # remove used node as gate
                config.Astar_netlist.used_nodes.remove((destination_node.x,
                                                        destination_node.y,
                                                        destination_node.z))

                return path[::-1], cost

            # skip Node if already visited
            if (current.x, current.y, current.z) in visited:
                continue
            visited.add((current.x, current.y, current.z))

            # Moves, checks if move is not out of bounds, then adds new Node
            # to heap with its parent Node.
            # NOTE: is another way for the next_move func. Total possibilities
            #       are 3! = 6.
            for dx, dy, dz in [ (1, 0, 0), (-1, 0, 0), (0, 1, 0), 
                                (0, -1, 0), (0, 0, 1), (0, 0, -1)]:
                x, y, z = current.x + dx, current.y + dy, current.z + dz
                if not (0 <= x <= grid_rows and 0 <= y <= grid_cols):
                    continue
                
                if not 0 <= z <= grid_layers:
                    continue
                                
                # INVALID NODE IF GATE NODE
                if (x, y, z) in config.Astar_netlist.gate_locations:
                    continue
                
                # skip if connection already occupied
                nodes_connection = {(current.x, current.y, current.z), 
                                    (x, y, z) }
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
        config.Astar_netlist.gate_locations.add((   destination_node.x,
                                                    destination_node.y,
                                                    destination_node.z) )

        # Return no path found
        return (None, None)
