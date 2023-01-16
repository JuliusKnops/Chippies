
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d 
#import matplotlib

#import matplotlib.rcsetup as rcsetup

"""matplotlib.use("TkAgg")
print(rcsetup.all_backends)
print(matplotlib.matplotlib_fname())"""

#col= (np.random.random(), (np.random.random()), (np.random.random()))
fig = plt.figure()

ax = fig.add_subplot(projection= "3d")
ax.set_xlim(0, 7); ax.set_ylim(0, 7); ax.set_zlim(0, 7)

example = [ [(1, 5, 0), (2, 5, 0), (3, 5, 0), (4, 5, 0), (5,5,0),(6,5,0)], 
[(1,5,0), (1, 4, 0), (2, 4, 0), (3, 4, 0), (4, 4, 0)],
[(4,4,0), (4, 3, 0), (3, 3, 0), (2, 3, 0), (1, 3, 0), (0, 3, 0), (0, 2, 0), (0, 1, 0), (0, 0, 0), (1, 0, 0), (2, 0, 0), (3,0,0), (3,1,0)],
[(6,2,0), (5, 2, 0), (5, 3, 0), (5, 4, 0), (6, 4, 0), (6,5,0)], 
[(3,1,0), (4, 1, 0), (5, 1, 0), (6, 1, 0), (7, 1, 0), (7,2,0), (6,2,0)]
]

for i in example:
    x_unit = []
    y_unit = []
    z_unit = []
    for j in i:
        x_unit.append(j[0])
        y_unit.append(j[1])
        z_unit.append(j[2])
    print(x_unit, y_unit, z_unit)
    ax.plot(x_unit, y_unit, z_unit)
plt.show()


#Matplotlib hardcode suboptimal example chip 0
fig = plt.figure()

ax = fig.add_subplot(projection= "3d")
ax.set_xlim(0, 7); ax.set_ylim(0, 7); ax.set_zlim(0, 7)
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

[(1,5,0), (1, 4, 0), (2, 4, 0), (3, 4, 0), (4, 4, 0)]

x_unit = [4, 4, 3, 2, 1, 0, 0, 0, 0, 1, 2, 3, 3]
y_unit = [4, 3, 3, 3, 3, 3, 2, 1, 0, 0, 0, 0, 1]
z_unit = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
ax.plot(x_unit, y_unit, z_unit, c='yellow')

[(4,4,0), (4, 3, 0), (3, 3, 0), (2, 3, 0), (1, 3, 0), (0, 3, 0), (0, 2, 0), (0, 1, 0), (0, 0, 0), (1, 0, 0), (2, 0, 0), (3,0,0), (3,1,1)]

x_unit = [6, 5, 5, 5, 6, 6]
y_unit = [2, 2, 3, 4, 4, 5]
z_unit = [0, 0, 0, 0, 0, 0]
ax.plot(x_unit, y_unit, z_unit, c='purple')

[(6,2,0), (5, 2, 0), (5, 3, 0), (5, 4, 0), (6, 4, 0), (6,5,0)]


x_unit = [3, 4, 5, 6, 7, 7, 6]
y_unit = [1, 1, 1, 1, 1, 2, 2]
z_unit = [0, 0, 0, 0, 0, 0, 0]
ax.plot(x_unit, y_unit, z_unit, c='purple')

[(3,1,0), (4, 1, 0), (5, 1, 0), (6, 1, 0), (7, 1, 0), (7,2,0), (6,2,0)]


plt.show()
