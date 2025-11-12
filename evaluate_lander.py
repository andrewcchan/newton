import gymnasium as gym
from stable_baselines3 import A2C
from stable_baselines3.common.vec_env import VecVideoRecorder, DummyVecEnv

# Create the environment
env_id = "LunarLander-v2"
video_folder = "logs/videos/"
video_length = 1000

env = DummyVecEnv([lambda: gym.make(env_id, render_mode="rgb_array")])

# Record the video
env = VecVideoRecorder(env, video_folder,
                       record_video_trigger=lambda x: x == 0, video_length=video_length,
                       name_prefix=f"a2c-{env_id}")

# Load the trained agent
model = A2C.load("a2c_lunar_lander", env=env)

# Evaluate the agent
obs = env.reset()
for _ in range(video_length + 1):
    action, _states = model.predict(obs, deterministic=True)
    obs, _, _, _ = env.step(action)

# Close the environment
env.close()
