# NOTE: Gate object not exactly the same as node object
class Gates():
    def __init__(self, name, x_coordinate, y_coordinate, z_coordinate):
        self.x = int(x_coordinate)
        self.y = int(y_coordinate)
        self.z = int(z_coordinate)
        self.name = name  
        self.connections = set()
    
    def add_connections(self, NewPoint):
        self.connections.add(NewPoint)
    
    def get_coordinates(self):
        return (self.x, self.y, self.z)
