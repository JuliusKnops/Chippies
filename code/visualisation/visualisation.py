import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d 

import csv

def visualisation(solution, chip_nr):
    """function for visualising chips

    Args:
        solution (list): list of all pathways
        gates (list): list with coördinates of gates
        chip_nr (int): number of chip to indicate dimensions
    """    
    #Plot 3d grid with dimensions 0 to 7 or 0 to 17
    fig = plt.figure()
    ax = fig.add_subplot(projection= "3d")
    if chip_nr == 0:
        ax.set_xlim(0, 7); ax.set_ylim(0, 7); ax.set_zlim(0, 7)
    elif chip_nr == 1: 
        ax.set_xlim(0, 18); ax.set_ylim(0, 18); ax.set_zlim(0, 7)
    else:
        ax.set_xlim(0, 18); ax.set_ylim(0, 18); ax.set_zlim(0, 7)
    # add labels 
    ax.set_xlabel("X-axis"); ax.set_ylabel("Y-axis"); ax.set_zlabel("Z-axis")

    # # place gates 
    # x_gates = []
    # y_gates = []
    # for i in gates:
    #     x_gates.append(i[0])
    #     y_gates.append(i[1])
    # ax.scatter(x_gates, y_gates, c='red', s=25)

    # append coördinates in right list for the pathways
    x_gates = []
    y_gates = []
    for i in solution:
        x_unit = []
        y_unit = []
        z_unit = []
        startgate = i[0]
        endgate = i[-1]
        x_gates.append(startgate[0])
        y_gates.append(startgate[1])
        x_gates.append(endgate[0])
        y_gates.append(endgate[1])
        for j in i:
            x_unit.append(j[0])
            y_unit.append(j[1])
            z_unit.append(j[2])
        ax.plot(x_unit, y_unit, z_unit)
    ax.scatter(x_gates, y_gates, c='red', s=25)

    # plot figure
    plt.savefig(f"{chip_nr}_solution.png")
    plt.show()


def create_histogram(chip_nr, netlist_nr):
    cost_list = []
    with open(f'chip_{chip_nr}_{netlist_nr}.csv', 'r', encoding='UTF8') as f:
        csv_reader = csv.reader(f)

        for row in csv_reader:
            try:
                cost_list.append(int(row[0]))
            except:
                pass
    
    plt.clf()
    plt.hist(cost_list, 10)
    plt.title(f"Chip: {chip_nr} netlist: {netlist_nr}")
    plt.savefig(f"{chip_nr} {netlist_nr}.png")