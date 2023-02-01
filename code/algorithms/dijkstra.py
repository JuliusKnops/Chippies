from . import Astar

class Node_dijkstra(Astar.Node_Astar):
    def __init__(self, x: int, y: int, z: int, cost = 0, parent = None) -> None:
        super().__init__(x, y, z, cost, parent)

    def __lt__(self, other):
        """
        Finds the cheapest node only by using path cost and no heuristics.
        """
        return self.cost < other.cost

class PathFinder_dijkstra(Astar.PathFinder_Astar):
    """
    This class is the same as Astar with the difference being that dijkstra
    does not use an estimation heuristics g(x).
    """
    def __init__(self, Start_chip: object, End_chip:object,
                auto_pathfind=True,
                Node = Node_dijkstra) -> None:
        super().__init__(Start_chip, End_chip, auto_pathfind=True, Node = Node)
