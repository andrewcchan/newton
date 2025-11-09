import gymnasium as gym
from stable_baselines3 import DQN

# Create the environment
env = gym.make("LunarLander-v3", render_mode="rgb_array")

# Instantiate the agent
model = DQN("MlpPolicy", env, verbose=1)

# Train the agent
model.learn(total_timesteps=100000, progress_bar=True)

# Save the agent
model.save("dqn_lunar_lander")

# Close the environment
env.close()
