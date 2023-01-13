class Gates():
    def __init__(self, x_coordinate, y_coordinate, name):
        self.x = x_coordinate
        self.y = y_coordinate
        self.name = name
        self.connections = set()
    
    def add_connections(self, NewPoint):
        self.connections.add(NewPoint)
