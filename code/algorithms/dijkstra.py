from . import Astar

class Node_dijkstra(Astar.Node_Astar):
    def __init__(self, x, y, z, cost = 0, parent = None):
        super().__init__(x, y, z, cost, parent)

    # No estimation
    def __lt__(self, other):
        return self.cost < other.cost

class PathFinder_dijkstra(Astar.PathFinder_Astar):
    def __init__(self, Start_chip, End_chip, auto_pathfind=True, Node = Node_dijkstra):
        super().__init__(Start_chip, End_chip, auto_pathfind=True, Node = Node)
