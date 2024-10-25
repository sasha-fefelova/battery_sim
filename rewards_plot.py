import json
import csv
import matplotlib.pyplot as plt

TEST = False # plot testing data (not training data)


type = "train"
if TEST:
    type = "test"

# rewards
with open(type + "_performance/rewards.json", "r") as file:
    file_reader = json.load(file)
 # "bo" to plot as dots

num_reward_points = len(file_reader)
original_price_data = []
with open("battery_data/rt_fivemin_hrl_lmps.csv", "r") as file:
    price_data_reader = csv.reader(file)
    i = 0
    first = True
    
    for price in price_data_reader:
        if first: 
            first = False
            continue
        # if i >= num_reward_points: #TODO - right now doesn't work if more data than five min prices
        #     break
        original_price_data.append(float(price[9])/10) # TODO - remove /10 
        i += 1
    print("DATA READER LENGTH: ", i)
price_data = []
for i in range(num_reward_points):
    price_data.append(original_price_data[i % len(original_price_data)])

with open(type + "_performance/actions_taken.json", "r") as file:
    action_file_reader = json.load(file)
actions = []
for action in action_file_reader:
    actions.append((action / 4 - 1) * 50)
# print(price_data)

print("total profit: ", sum(file_reader))
print(len(actions))
plt.axis()
plt.plot(actions, "green", linewidth = 0.5)
plt.plot(price_data, "blue", linewidth = 0.5)
plt.plot(file_reader, "red", linewidth = 0.5) # rewards
plt.show()

# average rewards
with open(type + "_performance/rewards.json", "r") as file:
    file_reader = json.load(file)
plt.plot(file_reader) # "bo" to plot as dots
total_rewards = []
total_reward = 0
plt.show()
for reward in file_reader:
    total_reward += reward
    total_rewards.append(total_reward)
plt.plot(total_rewards)

plt.show()

# average rewards
with open(type + "_performance/average_rewards.json", "r") as file:
    file_reader = json.load(file)
plt.plot(file_reader) # "bo" to plot as dots
plt.show()
