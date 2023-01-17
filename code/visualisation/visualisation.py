import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d 


def visualisation(self, gates, pathway):
        
    #Plot 3d grid with dimensions 0 to 7 
    fig = plt.figure()
    ax = fig.add_subplot(projection= "3d")
    ax.set_xlim(0, 7); ax.set_ylim(0, 7); ax.set_zlim(0, 7)

    # place gates 
    x_gates = []
    y_gates = []
    for i in gates:
        x_gates.append(i[1])
        y_gates.append(i[2])
        ax.scatter(x_gates, y_gates, c='red', s=100)

    example = [ [(1, 5, 0), (2, 5, 0), (3, 5, 0), (4, 5, 0), (5,5,0),(6,5,0)], 
    [(1,5,0), (1, 4, 0), (2, 4, 0), (3, 4, 0), (4, 4, 0)],
    [(4,4,0), (4, 3, 0), (3, 3, 0), (2, 3, 0), (1, 3, 0), (0, 3, 0), (0, 2, 0), (0, 1, 0), (0, 0, 0), (1, 0, 0), (2, 0, 0), (3,0,0), (3,1,0)],
    [(6,2,0), (5, 2, 0), (5, 3, 0), (5, 4, 0), (6, 4, 0), (6,5,0)], 
    [(3,1,0), (4, 1, 0), (5, 1, 0), (6, 1, 0), (7, 1, 0), (7,2,0), (6,2,0)]
    ]

    for i in pathway:
        x_unit = []
        y_unit = []
        z_unit = []
        for j in i:
            x_unit.append(j[0])
            y_unit.append(j[1])
            z_unit.append(j[2])
        ax.plot(x_unit, y_unit, z_unit)
    plt.show()


