import gymnasium as gym
from stable_baselines3 import A2C

# Create the environment
env = gym.make("LunarLander-v2", render_mode="rgb_array")

# Instantiate the agent
model = A2C("MlpPolicy", env, verbose=1)

# Train the agent
model.learn(total_timesteps=100000, progress_bar=True)

# Save the agent
model.save("a2c_lunar_lander")

# Close the environment
env.close()
