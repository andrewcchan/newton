import numpy as np

class RLAgent:
    def __init__(self, simulation_env):
        self.env = simulation_env

        # Discretize state space (gravity)
        self.gravity_bins = np.linspace(5, 15, 10)

        # Discretize action space (velocity and angle)
        self.velocity_bins = np.linspace(10, 30, 10)
        self.angle_bins = np.linspace(30, 60, 10)

        self.q_table = np.zeros((len(self.gravity_bins), len(self.velocity_bins), len(self.angle_bins)))

        self.alpha = 0.1
        self.gamma = 0.99
        self.epsilon = 1.0
        self.epsilon_decay = 0.995
        self.min_epsilon = 0.01

    def get_state(self, gravity):
        return np.digitize(gravity, self.gravity_bins) - 1

    def choose_action(self, state):
        if np.random.rand() < self.epsilon:
            return (np.random.choice(len(self.velocity_bins)),
                    np.random.choice(len(self.angle_bins)))
        return np.unravel_index(np.argmax(self.q_table[state]),
                                (len(self.velocity_bins), len(self.angle_bins)))

    def update_q_table(self, state, action, reward, next_state):
        v_idx, a_idx = action
        old_value = self.q_table[state, v_idx, a_idx]

        if next_state is None:
            next_max = 0
        else:
            next_max = np.max(self.q_table[next_state])

        new_value = old_value + self.alpha * (reward + self.gamma * next_max - old_value)
        self.q_table[state, v_idx, a_idx] = new_value

    def decay_epsilon(self):
        if self.epsilon > self.min_epsilon:
            self.epsilon *= self.epsilon_decay

    def get_action_values(self, action):
        v_idx, a_idx = action
        return self.velocity_bins[v_idx], self.angle_bins[a_idx]
