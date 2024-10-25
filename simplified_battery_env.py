# reference: 
# https://stable-baselines.readthedocs.io/en/master/guide/custom_env.html
# import gym
import gymnasium as gym
from gymnasium import spaces
import pybamm
import numpy as np
import datetime
import time

class BatteryEnv(gym.Env):
#   metadata = {'render.modes': ['human']}

    def __init__(self, time_step):
        print("in init")
        super(BatteryEnv, self).__init__()
        self.action_space = spaces.Discrete(3) # charge, discahrge, rest
        self.observation_space = spaces.Box(low = 0, high = 1, shape = (1,), dtype = float)
        self.render_mode = None
        self.prev_solution = None
        self.time_step = 0

    def reset(self, seed = None, options = None):
        print("in reset")
        # self.model = pybamm.lithium_ion.DFN()
        # experiemnt = pybamm.Experiment([("Discharge at C/10 for 1 hours or until 3V")])
        # self.sim = pybamm.Simulation(self.model, experiment = experiemnt)
        # solution = self.sim.solve(starting_solution = self.prev_solution)
        self.prev_solution = 0.3
        # self.prev_solution = solution
        # solution = None
        print("solution in reset: ", self.prev_solution)
        discharge_capacity = self.prev_solution

        return (np.array([discharge_capacity]), {})
        # return observation  # reward, done, info can't be included

    def step(self, action):
        self.time_step += 1
        # if self.time_step % 10 == 0:
        #     first_time = time.perf_counter()
        # todo save to file every approx 100 iterations and have a program to plot from that file
        
        # if self.time_step % 20 == 0:
        #     print("in step, action: ", action, " time step: ", self.time_step, " prev solution: ", self.prev_solution)
        if self.time_step % 1000 == 0:
            print("in step, action: ", action, " time step: ", self.time_step, " prev solution: ", self.prev_solution)
            # self.sim.plot(['Discharge capacity [A.h]'])
            # self.sim.save("intermediate_sim/intermediate_sim")
        battery_action = ""
        new_discharge_capacity = self.prev_solution
        reward = -1
        if action == 0: # discharge
            new_discharge_capacity -= 0.01
            reward -= 0.25
            battery_action = "Discharge at C/3 for 0.5 minute or until 3V"
        elif action == 1:
            new_discharge_capacity = new_discharge_capacity
            battery_action = "Rest for 0.5 minute"    
        elif action == 2:
            new_discharge_capacity += 0.01
            reward -= 0.25
            battery_action = "Charge at C/3 for 0.5 minute"
        else:
            print("INVALID ACTION")
        if self.time_step % 10 == 0:
            before_time = time.perf_counter()

        # experiemnt = pybamm.Experiment([(battery_action)])
        # if self.time_step % 10 == 0:
        #     print("setting up experiment: ",  time.perf_counter() - before_time)
        #     before_time = time.perf_counter()

        # self.sim = pybamm.Simulation(self.model, experiment = experiemnt)
        # if self.time_step % 10 == 0:
        #     print("setting up simulation: ",  time.perf_counter() - before_time)
        #     before_time = time.perf_counter()
        # try:
        #     solution = self.sim.solve(starting_solution = self.prev_solution)
        #     # solution = self.sim.solve(starting_solution = None)
        # except:
        #     print("solver issue")
        #     self.sim.plot(['Discharge capacity [A.h]'])
        #     solution = self.sim.solve(starting_solution = self.prev_solution)
        # if self.time_step % 10 == 0:
        #     print("solving: ",  time.perf_counter() - before_time)
        #     before_time = time.perf_counter()


        
        self.prev_solution = new_discharge_capacity
        reward = 0
        discharge_capacity = new_discharge_capacity
        # if discharge_capacity < 0.75 and discharge_capacity > 0.25:
        #     reward = 0
        if discharge_capacity < 0.6 and discharge_capacity > 0.5:
            reward = 1
        done = False
        if discharge_capacity < 0.01 or discharge_capacity > 0.99:
            print("DONE")
            done = True
        info = "info?"
        # if self.time_step % 10 == 0:
        #     print("full time step: ",  time.perf_counter() - first_time)
        return np.array([discharge_capacity]), reward, done, False, {}
        
        # return observation, reward, done, info
    
    def render(self, mode='human'):
        print("NO RENDERING")
    def close (self):
        # self.plot(['Discharge capacity [A.h]'])
        pass