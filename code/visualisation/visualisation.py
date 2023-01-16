
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d 


#Matplotlib hardcode suboptimal example chip 0
fig = plt.figure()

ax = fig.add_subplot(projection= "3d")
ax.set_xlim(0, 7); ax.set_ylim(0, 7); ax.set_zlim(0, 7)

# place gates 
x = [1,6,4,6,3]
y = [5,5,4,2,1]
z = [0,0,0,0,0]

ax.scatter(x, y, z, c='red', s=100)
x_unit = [1, 2, 3, 4, 5, 6]
y_unit = [5, 5, 5, 5, 5, 5]
z_unit = [0, 0, 0, 0, 0, 0]
ax.plot(x_unit, y_unit, z_unit, c='blue')

x_unit = [1, 1, 2, 3, 4]
y_unit = [5, 4, 4, 4, 4]
z_unit = [0, 0, 0, 0, 0]
ax.plot(x_unit, y_unit, z_unit, c='green')

x_unit = [4, 4, 3, 2, 1, 0, 0, 0, 0, 1, 2, 3, 3]
y_unit = [4, 3, 3, 3, 3, 3, 2, 1, 0, 0, 0, 0, 1]
z_unit = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
ax.plot(x_unit, y_unit, z_unit, c='yellow')

x_unit = [6, 5, 5, 5, 6, 6]
y_unit = [2, 2, 3, 4, 4, 5]
z_unit = [0, 0, 0, 0, 0, 0]
ax.plot(x_unit, y_unit, z_unit, c='purple')

x_unit = [3, 4, 5, 6, 7, 7, 6]
y_unit = [1, 1, 1, 1, 1, 2, 2]
z_unit = [0, 0, 0, 0, 0, 0, 0]
ax.plot(x_unit, y_unit, z_unit, c='purple')

plt.show()