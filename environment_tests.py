# TESTING STRATEGY

# the following behaviors should be tested:
# charging / discharging at soc limits
# different powers - in general should take 2/4 times longer to reach limits for 1, 0.5, 0.25

import gymnasium as gym
from gymnasium import spaces
import numpy as np
import csv
import pybamm
import matplotlib.pyplot as plt

from stable_baselines3.common.env_util import make_vec_env, DummyVecEnv
from stable_baselines3 import PPO
from environments.battery_env import BatteryEnv

SIMPLIFIED = True

# set up the initial battery
def make_initial_battery(): 
    model = pybamm.lithium_ion.SPM()
    sim_discharge = pybamm.Simulation(model, experiment = [("Discharge at 0C for " + str(1) + " minutes")])
    sim_discharge.build_for_experiment()
    solution = sim_discharge.solve(initial_soc = 0.5)
    soc = -solution["Discharge capacity [A.h]"].entries[-1] + 0.5 # soc change + initial soc
    return solution, soc


# get (last day of the week) prices to use for prediction - same data test_battery_ppo tests on, so can compare total profits
electricity_prices = []
with open("battery_data/rt_fivemin_hrl_lmps.csv") as file:
    rows = csv.reader(file)
    first = True
    for row in rows:
        if first: 
            first = False
            continue
        if float(row[1][2:4]) == 21:
            electricity_prices.append(float(row[9]))


initial_battery, init_soc = make_initial_battery()
print("initial soc: ", init_soc)

action_space  = spaces.Discrete(9)
env = BatteryEnv(initial_battery, training = False, prices = electricity_prices, initial_soc = init_soc, simplified = SIMPLIFIED) 
vec_env = DummyVecEnv([lambda: env])
model = PPO.load("simplified_models/final_battery_model_ppo", env) # CHANGE FILE TO LOAD HERE
model.set_env(env)

all_soc = []
obs = vec_env.reset()
total_reward = 0


for i in range(288): # 2 days, last day repeated twice
    price = electricity_prices[i % len(electricity_prices)]
    print("iteration: ", i, " expected price: ", price, " obs: ", obs)

    # different tests here
    action = action_space.sample(mask = np.array([1, 0, 0, 0, 0, 0, 0, 0, 0], dtype = np.int8)) # discharge 1 W
    # action = action_space.sample(mask = np.array([0, 0, 0, 1, 0, 0, 0, 0, 0], dtype = np.int8)) # discharge 0.25 W
    # action = action_space.sample(mask = np.array([0, 0, 0, 0, 1, 0, 0, 0, 0], dtype = np.int8)) # no power
    # action = action_space.sample(mask = np.array([0, 0, 0, 0, 0, 0, 1, 0, 0], dtype = np.int8)) # charge 0.5 W
    
    # simple policy: discharge at 1W at price 45 and above, charge below
    if price >= 28.5:
        action = action_space.sample(mask = np.array([1, 0, 0, 0, 0, 0, 0, 0, 0], dtype = np.int8)) # discharge 1 W
    else:
        action = action_space.sample(mask = np.array([0, 0, 0, 0, 0, 0, 0, 0, 1], dtype = np.int8)) # discharge 1 W


    obs, reward, done, info = vec_env.step([action])
    if done:
        print("DONE")
        break
    if SIMPLIFIED:
        all_soc.append(obs[0][1])
    else:
        all_soc.append(obs[0][3])
    total_reward += reward



vec_env.close()
print("total reward: ", total_reward)
plt.plot(all_soc)
plt.show()