from simulation import Simulation
from rl_agent import RLAgent
import numpy as np
import matplotlib.pyplot as plt
import imageio

# --- Setup ---
TARGET = {"x": 40, "y": 10, "radius": 2}
env = Simulation(TARGET)
agent = RLAgent(env)
episodes = 2000

print("--- Training Agent ---")
# --- Training Phase ---
for episode in range(episodes):
    gravity = np.random.uniform(5, 15)
    state = agent.get_state(gravity)

    action = agent.choose_action(state)
    velocity, angle = agent.get_action_values(action)

    result = env.run(velocity, angle, gravity)
    reward = 1 if result["hit"] else -1

    # Update Q-table (terminal state, so no next_state)
    agent.update_q_table(state, action, reward, None)
    agent.decay_epsilon()

    if (episode + 1) % 100 == 0:
        print(f"Episode {episode + 1}/{episodes} complete.")

print("--- Training Complete ---")

# --- Save Q-table ---
np.save("q_table.npy", agent.q_table)
print("--- Q-table saved to q_table.npy ---")
