import gymnasium as gym

from stable_baselines3 import PPO
from environments.battery_env import BatteryEnv
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.callbacks import CheckpointCallback, BaseCallback, EveryNTimesteps
from stable_baselines3.common.callbacks import ProgressBarCallback
from stable_baselines3.common.utils import set_random_seed
from stable_baselines3.common.env_util import make_vec_env, DummyVecEnv


import pybamm

# TODO - make this callback work
# class SaveStateCallback(BaseCallback):
#     def __init__(self, env):
#         print("added env")
#         self.env = env
#         super().__init__()
    

#     def _on_step(self):
#         self.env.env_method("save_state")

CONTINUE_TRAINING = False
render_mode = None
CHECK_ENV = False # tests correctness of environment setup - generally should be false unless making major changes to the environment
# RANDOM_SEED = 123214213 TODO - set up random seed selection (fixed, different for each env)
SIMPLIFIED = True # True --> using simplified environment that does not use PyBaMM
path = "models" # simplified_models for simplified env
prefix = "battery_model"
if SIMPLIFIED:
    path = "simplified_" + path
    prefix = "simplified_" + prefix



# test function for making an initial battery, but later an aged second-life battery will be used
# second life battery final solution and final soc will be loaded from the file instead of calling this function
def make_initial_battery(): # in the future use aged second life batteries
    model = pybamm.lithium_ion.SPM()
    sim_discharge = pybamm.Simulation(model, experiment = [("Discharge at 0C for " + str(1) + " minutes")])
    sim_discharge.build_for_experiment()
    solution = sim_discharge.solve(initial_soc = 0.5)
    soc = -solution["Discharge capacity [A.h]"].entries[-1] + 0.5 # soc change + initial soc
    return solution, soc


# get the initial battery and set up initial environment
initial_battery, initial_soc = make_initial_battery()
env = make_vec_env(lambda: BatteryEnv(initial_battery, initial_soc, simplified = SIMPLIFIED), n_envs = 4, seed = 123) # 4 environemnts in parallel


if CHECK_ENV:
    check_env(env)

# set up callbacks
model_save_callback = CheckpointCallback(save_freq=1_000_00, save_path=path, name_prefix = prefix) # saves the model in the middle of trainig
# state_save_callback = EveryNTimesteps(n_steps = 50, callback = SaveStateCallback(env)) TODO



if CONTINUE_TRAINING: # continue training from an existing model
    model = PPO.load(path + "/training_battery_model_ppo", env)
    model.set_env(env)
else: # start training
    model = PPO("MlpPolicy", env, verbose=1)

# train
model.learn(total_timesteps=500000, progress_bar = True, callback = [model_save_callback]) # TODO change to [model_save_callback, state_save_callback]

env.close()

# save the final model

final_path = "models/final_battery_model_ppo"
if SIMPLIFIED:
    final_path = "simplified_" + final_path
model.save(final_path)
print("done")
