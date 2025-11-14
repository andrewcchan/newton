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

# --- Visualization Phase ---
print("--- Generating Performance Video ---")
# Disable exploration for visualization
agent.epsilon = 0.0

performance_data = []
# Test the agent on a range of gravity values
gravity_constants = np.linspace(5, 15, 20)

for gravity in gravity_constants:
    state = agent.get_state(gravity)
    action = agent.choose_action(state) # Will choose the best action
    velocity, angle = agent.get_action_values(action)
    result = env.run(velocity, angle, gravity)
    performance_data.append((result, gravity, velocity, angle))

# --- Video Generation ---
fig, ax = plt.subplots()

def animate_performance(i):
    ax.clear()

    result, gravity, velocity, angle = performance_data[i]
    x, y, target = result["x"], result["y"], result["target"]

    ax.plot(x, y, label=f"V:{velocity:.1f} m/s, A:{angle:.1f}°")
    target_circle = plt.Circle((target["x"], target["y"]), target["radius"], color="r", label="Target")
    ax.add_patch(target_circle)

    ax.set_xlim(0, 60)
    ax.set_ylim(0, 40)
    title = f"Gravity: {gravity:.2f} m/s², Hit: {result['hit']}"
    ax.set_title(title)
    ax.legend()

writer = imageio.get_writer("trained_agent_performance.mp4", fps=2)

for i in range(len(performance_data)):
    animate_performance(i)
    fig.canvas.draw()
    image = np.frombuffer(fig.canvas.tostring_argb(), dtype='uint8')
    image = image.reshape(fig.canvas.get_width_height()[::-1] + (4,))
    image = image[..., :3] # Convert ARGB to RGB
    writer.append_data(image)

writer.close()
plt.close()

print("--- Video 'trained_agent_performance.mp4' saved. ---")
