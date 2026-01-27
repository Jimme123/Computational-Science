import json
import matplotlib.pyplot as plt

with open("rollingstock_result.json", 'r') as fp:
    data = json.load(fp)

sprinter_data = data["sprinter"]
max_trains = 25

num_trains = [0]
static_capacity = [0]
moving_capacity = [0]
i = 0
for measurement in sprinter_data['wide']:
    num_trains.append(measurement[0])
    static_capacity.append(measurement[1][0][0])
    moving_capacity.append(measurement[1][0][1])
    i += 1
    if i >= max_trains:
        break

plt.figure(figsize=(10,6))
plt.plot(num_trains, static_capacity, label="Max Static Capacity", marker='o', color="cornflowerblue")
plt.plot(num_trains, moving_capacity, label="Max Moving Capacity", marker='x', color="indianred")
# Hardcoded lines to indicate Level off
plt.plot([8, 8], [-10, 100], marker='', linestyle='dashed', color="cornflowerblue")
plt.plot([12, 12], [-10, 100], marker='', linestyle='dashed', color="indianred")
plt.ylim(0, 45)
plt.xlabel("Number of trains", fontsize=15)
plt.ylabel("Capacity", fontsize=15)
plt.title("Capacity per Number of Trains", fontsize=15)
plt.legend()
plt.grid(True)
plt.savefig("../plots/capacity_per_train.png", bbox_inches="tight", dpi=300)
plt.show()