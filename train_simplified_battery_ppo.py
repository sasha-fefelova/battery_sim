import gymnasium as gym

from stable_baselines3 import PPO
from simplified_battery_env import BatteryEnv
from stable_baselines3.common.env_checker import check_env


CONTINUE_TRAINING = False


render_mode = None

print("before made env")

env = BatteryEnv(0.5)
reset_returns = env.reset()
print("right before assertion: ", type(reset_returns))
assert isinstance(reset_returns, tuple)

check_env(env)
# env = gym.make(ENV, render_mode=render_mode)
print("after made env")


if CONTINUE_TRAINING:
    model = PPO.load("models/cartpole_model_ppo")
    model.set_env(env)
else: 
    print("before creating model")
    model = PPO("MlpPolicy", env, verbose=1)
print("right before learning")


model.learn(total_timesteps=100_000)

env.close()
model.save("models/battery_model_ppo")
