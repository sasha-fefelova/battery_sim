import gymnasium as gym
import numpy as np
import csv
import pybamm

from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env, DummyVecEnv
# from real_battery_env import BatteryEnv
from environments.simplified_battery_env import BatteryEnv


def make_initial_battery(): # in the future use aged second life batteries
    model = pybamm.lithium_ion.SPM()
    sim_discharge = pybamm.Simulation(model, experiment = [("Discharge at C/10 for " + str(60) + " minutes")])
    sim_discharge.build_for_experiment()
    solution = sim_discharge.solve()
    return solution


# get (last day of the week for now) prices to use for prediction
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


# set up the environemnt
initial_battery = make_initial_battery()
env = BatteryEnv(initial_battery, training = False, prices = electricity_prices, initial_soc = 0.6) # NOT IDEAL TODO - fix
model = PPO.load("toy_models/new_battery_model_ppo", env)
model.set_env(env)
vec_env = DummyVecEnv([lambda: env]) 

obs = vec_env.reset()

for i in range(288): # iterate though the days
    print("iteration: ", i)
    print("OBS: ", obs)
    action, _states = model.predict(obs, deterministic=True) # what action to take
    print("action: ", action)

    # take a step in the simulation
    obs, reward, done, info = vec_env.step(action)

    if done:
        print("DONE")
        break

vec_env.close() # close environment

