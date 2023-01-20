import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d 

#Plot 3d grid with dimensions 0 to 7 
fig = plt.figure()
ax = fig.add_subplot(projection= "3d")
ax.set_xlim(0, 7); ax.set_ylim(0, 7); ax.set_zlim(0, 7)

gates = [(1,5),(6,5),(4,4),(6,2),(3,1)]
# place gates 
x_gates = []
y_gates = []
for i in gates:
    x_gates.append(i[0])
    y_gates.append(i[1])
    ax.scatter(x_gates, y_gates, c='red', s=100)

example = 


for i in example:
    x_unit = []
    y_unit = []
    z_unit = []
    for j in i:
        x_unit.append(j[0])
        y_unit.append(j[1])
        z_unit.append(j[2])
    ax.plot(x_unit, y_unit, z_unit)
plt.show()

