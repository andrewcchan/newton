from simulation import Simulation
from rl_agent import RLAgent
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import imageio

# --- Training ---
TARGET = {"x": 40, "y": 10, "radius": 2}
env = Simulation(TARGET)
agent = RLAgent(env)

episodes = 500
training_data = []

for episode in range(episodes):
    gravity = np.random.uniform(5, 15)
    state = agent.get_state(gravity)

    action = agent.choose_action(state)
    velocity, angle = agent.get_action_values(action)

    result = env.run(velocity, angle, gravity)
    reward = 1 if result["hit"] else -1

    # Since each throw is a terminal state, the future reward is 0
    agent.update_q_table(state, action, reward, None)
    agent.decay_epsilon()

    training_data.append((result, gravity))

# --- Visualization ---
fig, ax = plt.subplots()

def animate(i):
    ax.clear()

    result, gravity = training_data[i]
    x, y, target = result["x"], result["y"], result["target"]

    ax.plot(x, y, label="Trajectory")
    target_circle = plt.Circle((target["x"], target["y"]), target["radius"], color="r", label="Target")
    ax.add_patch(target_circle)

    ax.set_xlim(0, 60)
    ax.set_ylim(0, 40)
    ax.set_title(f"Episode: {i+1}, Gravity: {gravity:.2f}, Hit: {result['hit']}")
    ax.legend()

writer = imageio.get_writer("rl_training.mp4", fps=10)

for i in range(len(training_data)):
    animate(i)
    fig.canvas.draw()
    image = np.frombuffer(fig.canvas.tostring_argb(), dtype='uint8')
    image = image.reshape(fig.canvas.get_width_height()[::-1] + (4,))
    image = image[..., :3]
    writer.append_data(image)

writer.close()
plt.close()
