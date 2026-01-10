
import gymnasium as gym
import stable_baselines3
import ale_py
import cv2
import numpy as np

print("All modules imported successfully.")
env = gym.make("BreakoutNoFrameskip-v4")
print("Environment created successfully.")
env.close()
