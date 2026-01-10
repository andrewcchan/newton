import gymnasium as gym
import ale_py
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_atari_env
from stable_baselines3.common.vec_env import VecFrameStack
import time

def visualize():
    gym.register_envs(ale_py)
    # Load the trained model
    model = PPO.load("breakout_ppo")

    # Create the environment for visualization
    # We use a single environment with render_mode='human' if we could see it,
    # but here we might just run it to verify it works without error.
    # In a headless environment, 'rgb_array' is safer or just None if we don't capture frames.
    env = make_atari_env("BreakoutNoFrameskip-v4", n_envs=1, seed=0)
    env = VecFrameStack(env, n_stack=4)

    obs = env.reset()
    total_reward = 0
    done = False

    print("Running evaluation...")
    # Run for 1000 steps or until done
    for _ in range(1000):
        action, _states = model.predict(obs)
        obs, rewards, dones, info = env.step(action)
        total_reward += rewards[0]
        # env.render("human") # Not available in headless usually
        if dones[0]:
            break

    print(f"Total Reward: {total_reward}")
    env.close()

if __name__ == "__main__":
    visualize()
