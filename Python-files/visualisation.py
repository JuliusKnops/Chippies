import csv
import numpy as np
import matplotlib.pyplot as plt
import ast
from mpl_toolkits import mplot3d 


with open("output.csv", 'r') as p:
    pathways = csv.reader(p)
    next(pathways)
    path_list = []
    for paths in pathways:
        path_list.append(ast.literal_eval(paths[1]))
    path_list.pop()

with open("Print_0.csv", 'r') as g:
    gates = csv.reader(g)
    next(gates)
    x_gate = []
    y_gate = []
    for gate in gates:
        x_gate.append(ast.literal_eval(gate[1]))
        y_gate.append(ast.literal_eval(gate[2]))

#Plot 3d grid with dimensions 0 to 7 
fig = plt.figure()
ax = fig.add_subplot(projection= "3d")
ax.set_xlim(0, 7); ax.set_ylim(0, 7); ax.set_zlim(0, 7)


# place gates 
ax.scatter(x_gate, y_gate, c='red', s=100)

# Print each pathway
for i in path_list:
    x_unit = []
    y_unit = []
    z_unit = []
    if path_list[2] == None:
        path_list[2] == 0
    for j in i:
        x_unit.append(j[0])
        y_unit.append(j[1])
        z_unit.append(0)
    ax.plot(x_unit, y_unit, z_unit)
plt.show()


