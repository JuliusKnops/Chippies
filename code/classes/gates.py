class Gates(): # Overerven van Node class
    def __init__(self, x_coordinate, y_coordinate, name):
        #super__init__(x, y)
        self.x = x_coordinate
        self.y = y_coordinate
        self.name = name
        self.connections = set()
    
    def add_connections(self, NewPoint):
        self.connections.add(NewPoint)
