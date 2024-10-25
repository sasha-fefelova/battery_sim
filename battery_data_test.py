import csv
import matplotlib.pyplot as plt
all_prices = []

with open("battery_data/rt_fivemin_hrl_lmps.csv") as file:
    rows = csv.reader(file)
    first = True
    for row in rows:
        if first: 
            first = False
            continue
        all_prices.append(float(row[9]))
plt.plot(all_prices)
plt.show()