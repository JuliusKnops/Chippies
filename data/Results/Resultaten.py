import json
import numpy as np
import matplotlib.pyplot as plt
import csv

result_files = [
'Astar_sample_1_1']
# ,
# 'Astar_sample_1_4',
# 'Astar_sample_2_3',
# 'Hillclimber_sample_0_1',
# 'SimulatedAnnealing_sample_2_9']


for results in result_files:
    print(f"RESULTS FILE = {results}")
    f = open(f"Results/{results}.json")

    data = json.load(f)
    

    hist = []

    for i in data.values():
        hist.append(i[1])

    f.close()

    plt.clf()
    plt.hist(hist, 10)
    plt.title(f"{results}")
    plt.savefig(f"{results}.png")

with open(f'Results/temp_resultaten/chip_1_1.csv', 'r', encoding='UTF8') as f:
    cost_list = []
    csv_reader = csv.reader(f)

    for row in csv_reader:
        try:
            cost_list.append(int(row[0]))
        except:
            pass
    
    plt.clf()
    plt.hist(cost_list, 10, label="Random Algorithm", color='b')
    plt.title(f"Chip 1: Costs with different algorithms")
    plt.xlabel("Cost of solution")
    plt.ylabel("Frequency")
    plt.axvline(375, ymax = 0.8, color='black', label="Best Simulated Annealing sample solution")
    plt.axvline(371, ymax = 0.8, color='r', label="Best A* sample solution")
    plt.axvline(971, ymax = 0.8, color='green', label="Best Hillclimber sample solution")
    lgd = plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
    plt.savefig(f"Chip2_Random.png", bbox_extra_artists=(lgd,), bbox_inches='tight')

