import pytest
import numpy as np
from rl_agent import RLAgent
from simulation import Simulation

TARGET = {"x": 40, "y": 10, "radius": 2}

@pytest.fixture
def agent():
    sim = Simulation(TARGET)
    return RLAgent(sim)

def test_get_state(agent):
    """Test that gravity values are correctly binned into discrete states."""
    # Test gravity at the lower bound
    assert agent.get_state(gravity=5.0) == 0
    # Test gravity at the upper bound
    assert agent.get_state(gravity=15.0) == len(agent.gravity_bins) - 1
    # Test a value in the middle
    gravity_mid = np.mean(agent.gravity_bins)
    expected_state = np.digitize(gravity_mid, agent.gravity_bins) - 1
    assert agent.get_state(gravity_mid) == expected_state

def test_choose_action_exploration(agent):
    """Test that the agent explores when epsilon is 1.0."""
    agent.epsilon = 1.0
    state = 0
    # Run multiple times to increase confidence that it's random
    actions = {agent.choose_action(state) for _ in range(50)}
    # With pure exploration, we expect to see multiple different actions chosen
    assert len(actions) > 1

def test_choose_action_exploitation(agent):
    """Test that the agent exploits the best action when epsilon is 0.0."""
    agent.epsilon = 0.0
    state = 0
    # Manually set a clear best action in the Q-table
    agent.q_table[state, 5, 5] = 100.0
    best_action = (5, 5)

    # Run multiple times to ensure it consistently chooses the best action
    for _ in range(10):
        assert agent.choose_action(state) == best_action

def test_update_q_table(agent):
    """Test that the Q-table is updated correctly."""
    state = 0
    action = (3, 4)
    reward = 1

    # Test update for a terminal state (next_state is None)
    old_q_value = agent.q_table[state, action[0], action[1]]
    agent.update_q_table(state, action, reward, next_state=None)
    new_q_value = agent.q_table[state, action[0], action[1]]

    # Expected value: old + alpha * (reward - old)
    expected_q_value = old_q_value + agent.alpha * (reward - old_q_value)
    assert np.isclose(new_q_value, expected_q_value)

def test_decay_epsilon(agent):
    """Test that epsilon decays correctly."""
    initial_epsilon = agent.epsilon
    agent.decay_epsilon()
    assert agent.epsilon < initial_epsilon
    assert agent.epsilon == initial_epsilon * agent.epsilon_decay
