import heapq

class Node:
    def __init__(self, x, y, z, cost, parent):
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
        return self.cost < other.cost

    # This functions checks if goal state is reached.
    # NOTE: without this function, eq seems to fail even when the cost and parent attribute match...?
    def __eq__(self, other):
        if self.x == other.x and self.y == other.y and self.z == other.z:
            return True
        return False

#######################
### Unfinished Astar
#######################
def astar(grid, start, end):
    heap = []

    # push first node into the heap
    heapq.heappush(heap, (0, start))

    visited = set()

    # while there are still nodes to check...
    while heap:
        # return smallest node from the heap stack
        current = heapq.heappop(heap)[1]

        # checks if goal node
        if current == end:
            path = []
            # returns the path and then reverse the order
            # NOTE: order start at the end and ends at the start.
            #       We visit each parent node until no parent node
            #       left, e.g. we reached the start.
            while current:
                path.append((current.x, current.y, current.z))
                current = current.parent
            return path[::-1]

        # skip Node if already visited
        if (current.x, current.y, current.z) in visited:
            continue
        visited.add((current.x, current.y, current.z))

        # Moves, checks if move is not out of bounds, then adds new Node
        # to heap with its parent Node.
        # NOTE: is another way for the next_move func. Total possibilities are
        # 3! = 6.
        for dx, dy, dz in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]:
            x, y, z = current.x + dx, current.y + dy, current.z + dz
            if not (0 <= x < grid_rows and 0 <= y < grid_cols and 0 <= z < grid_layers):
                continue

            cost = current.cost + 1
            heapq.heappush(heap, (cost, Node(x, y, z, cost, current)))
    
    raise Exception("Failed to find a path.")

if __name__ == '__main__':
    grid_rows = 2
    grid_cols = 2
    grid_layers = 1
    # 2x2 grid with only 1 layer
    grid = [
            [ # start of layer
            [[0, 0, 0], [0, 1, 0]], # X-axis row 1 
            [[1, 0, 0], [1, 1, 0]]  # X-axis row 2
                 ] # end of layer
                ]
    start = Node(0, 0, 0, 0, None)
    end = Node(1, 1, 0, 0, None)

    print(astar(grid, start, end))