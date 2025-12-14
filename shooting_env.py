import gymnasium as gym
from gymnasium import spaces
import numpy as np
from simulation import ProjectileSimulation

class ShootingEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"]}

    def __init__(self, render_mode=None):
        super(ShootingEnv, self).__init__()

        self.sim = ProjectileSimulation()

        # Action space: [angle, velocity] normalized to [-1, 1]
        # We will map this to real values in step()
        self.action_space = spaces.Box(low=-1.0, high=1.0, shape=(2,), dtype=np.float32)

        # Observation space: [target_x_normalized]
        self.observation_space = spaces.Box(low=0.0, high=1.0, shape=(1,), dtype=np.float32)

        self.target_x = 0.0
        self.max_target_dist = 450.0
        self.max_sim_dist = 1000.0 # Used for normalization if needed
        self.render_mode = render_mode

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        # Randomize target position between 50 and 450
        self.target_x = np.random.uniform(50, self.max_target_dist)

        # Return normalized observation
        obs = np.array([self.target_x / self.max_target_dist], dtype=np.float32)
        return obs, {}

    def step(self, action):
        # Unscale actions
        # action[0] is angle factor: [-1, 1] -> [0, 90]
        # action[1] is velocity factor: [-1, 1] -> [0, 100]

        # Using linear mapping:
        # angle = (act + 1) / 2 * (max - min) + min
        angle = (np.clip(action[0], -1, 1) + 1) / 2 * 90.0
        velocity = (np.clip(action[1], -1, 1) + 1) / 2 * 100.0

        landing_x, trajectory = self.sim.simulate(velocity, angle)

        distance = abs(landing_x - self.target_x)

        # Reward function
        # We want to minimize distance.
        # Max reasonable error is ~500.
        # Reward = 1.0 - (distance / 500.0)
        # If perfect hit: 1.0
        # If miss by 500m: 0.0
        # If miss by 1000m: -1.0

        reward = 1.0 - (distance / 500.0)

        terminated = True
        truncated = False

        info = {
            "landing_x": landing_x,
            "target_x": self.target_x,
            "distance": distance,
            "trajectory": trajectory,
            "angle": angle,
            "velocity": velocity
        }

        obs = np.array([self.target_x / self.max_target_dist], dtype=np.float32)

        return obs, reward, terminated, truncated, info
