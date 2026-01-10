import gymnasium as gym
import ale_py
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_atari_env
from stable_baselines3.common.vec_env import VecFrameStack
import os

def train():
    gym.register_envs(ale_py)
    # Create the environment
    # We use BreakoutNoFrameskip-v4 as it's the standard for Atari benchmarks
    # make_atari_env includes standard Atari wrappers (episodic life, fire reset, etc.)
    env = make_atari_env("BreakoutNoFrameskip-v4", n_envs=4, seed=0)

    # Stack 4 frames
    env = VecFrameStack(env, n_stack=4)

    # Initialize the PPO agent
    # CnnPolicy is used for image-based inputs
    model = PPO("CnnPolicy", env, verbose=1,
                learning_rate=2.5e-4,
                n_steps=128,
                batch_size=32,
                n_epochs=4,
                clip_range=0.1,
                ent_coef=0.01,
                vf_coef=0.5)

    print("Starting training...")
    # Train for 10,000 timesteps for verification purposes in this environment
    # To solve it properly, increase this to 10,000,000
    model.learn(total_timesteps=10000)
    print("Training finished.")

    # Save the model
    model.save("breakout_ppo")
    print("Model saved to breakout_ppo.zip")

    env.close()

if __name__ == "__main__":
    train()
