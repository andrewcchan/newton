import pytest
import numpy as np
from simulation import ProjectileSimulation
from shooting_env import ShootingEnv

def test_simulation_accuracy():
    sim = ProjectileSimulation()
    # Test case: 45 degrees, 10 m/s
    # Range = v^2 / g * sin(2*theta) = 100 / 9.81 * 1 = 10.193
    v = 10
    angle = 45
    landing_x, _ = sim.simulate(v, angle)
    expected_range = (v**2 * np.sin(np.radians(2*angle))) / 9.81
    assert np.isclose(landing_x, expected_range, atol=0.1)

def test_simulation_zero_velocity():
    sim = ProjectileSimulation()
    landing_x, _ = sim.simulate(0, 45)
    assert landing_x == 0.0

def test_simulation_vertical_shot():
    sim = ProjectileSimulation()
    # 90 degrees, should land at 0
    landing_x, _ = sim.simulate(10, 90)
    assert np.isclose(landing_x, 0.0, atol=1e-5)

def test_env_reset():
    env = ShootingEnv()
    obs, _ = env.reset()
    assert obs.shape == (1,)
    assert 0 <= obs[0] <= 1
    # Check target x denormalized
    target_x = env.target_x
    assert 50 <= target_x <= env.max_target_dist

def test_env_step():
    env = ShootingEnv()
    env.reset()
    # Action: 0 angle (mapped to 45 deg), 0 velocity (mapped to 50 m/s)
    # 0 in [-1, 1] maps to middle.
    action = np.array([0.0, 0.0], dtype=np.float32)
    obs, reward, terminated, truncated, info = env.step(action)

    assert terminated is True
    # Reward might be numpy float, check generic float
    assert isinstance(reward, (float, np.floating))
    assert "landing_x" in info
    assert "trajectory" in info
    assert len(info["trajectory"]) > 0
    assert info["angle"] == 45.0
    assert info["velocity"] == 50.0

def test_env_reward_hit():
    env = ShootingEnv()
    env.reset()
    target_x = 100.0
    env.target_x = target_x

    # Calculate velocity needed to hit 100m at 45 degrees
    # R = v^2 / g
    # v = sqrt(R * g) = sqrt(100 * 9.81) = sqrt(981) approx 31.32
    v_needed = np.sqrt(target_x * 9.81)

    # Map back to action space [-1, 1]
    # v_mapped = (action + 1) / 2 * 100 -> action = (v / 50) - 1
    action_v = (v_needed / 50.0) - 1.0
    action_angle = -1.0 + (45.0 / 45.0) # 0 maps to 45? No.
    # angle = (act + 1)/2 * 90 => act = angle/45 - 1. 45/45 - 1 = 0.
    action_angle = 0.0

    action = np.array([action_angle, action_v], dtype=np.float32)
    _, reward, _, _, info = env.step(action)

    # Check distance
    assert info["distance"] < 1.0 # Should be very close
    assert reward > 0.95 # close to 1
