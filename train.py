import gymnasium as gym
from stable_baselines3 import PPO
from shooting_env import ShootingEnv
import os

def train():
    # Create the environment
    env = ShootingEnv()

    # Initialize the agent
    # Use MlpPolicy.
    model = PPO("MlpPolicy", env, verbose=1, learning_rate=0.001)

    # Train the agent
    print("Training the agent...")
    model.learn(total_timesteps=100000)

    # Save the model
    model.save("ppo_shooting_agent")
    print("Model saved as ppo_shooting_agent.zip")

if __name__ == "__main__":
    train()
