import gymnasium as gym
from stable_baselines3 import PPO
from shooting_env import ShootingEnv
import matplotlib.pyplot as plt
import numpy as np
import imageio
import os

def visualize_and_save():
    env = ShootingEnv()
    model = PPO.load("ppo_shooting_agent")

    obs, _ = env.reset()
    target_x = obs[0] * 450.0 # Denormalize based on max_target_dist
    print(f"Target is at x={target_x:.2f}")

    action, _ = model.predict(obs, deterministic=True)

    # We need to manually calculate what the angle/velocity are for printing,
    # but the env does it in step info.

    # Run the step to get trajectory
    _, _, _, _, info = env.step(action)
    trajectory = info['trajectory']
    landing_x = info['landing_x']
    dist = info['distance']
    angle = info['angle']
    velocity = info['velocity']

    print(f"Agent chose Action={action}")
    print(f"Mapped to Angle={angle:.2f}, Velocity={velocity:.2f}")
    print(f"Landed at x={landing_x:.2f} (Distance: {dist:.2f})")

    # Create Frames for Animation
    frames = []

    # Setup plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, max(550, landing_x + 50))
    ax.set_ylim(0, max(300, max([p[1] for p in trajectory]) + 50))
    ax.set_xlabel("Distance (m)")
    ax.set_ylabel("Height (m)")
    ax.set_title(f"Projectile Motion (Target: {target_x:.1f}m)")
    ax.grid(True)

    # Static elements
    ax.scatter(target_x, 0, c='red', s=100, marker='x', label='Target')
    projectile_plot, = ax.plot([], [], 'bo-', markersize=6, label='Projectile')
    trajectory_line, = ax.plot([], [], 'b--', alpha=0.3)
    ax.legend()

    xs, ys = zip(*trajectory)

    for i in range(len(xs)):
        current_x = xs[:i+1]
        current_y = ys[:i+1]

        projectile_plot.set_data([xs[i]], [ys[i]]) # pass sequence
        trajectory_line.set_data(current_x, current_y)

        # Draw frame to numpy buffer
        fig.canvas.draw()

        # Extract image from canvas
        image = np.frombuffer(fig.canvas.buffer_rgba(), dtype='uint8')
        image = image.reshape(fig.canvas.get_width_height()[::-1] + (4,))
        image = image[:, :, :3] # RGBA to RGB

        frames.append(image)

    plt.close(fig)

    # Save as mp4 using imageio
    print("Saving animation to shooting_solution.mp4...")
    imageio.mimsave('shooting_solution.mp4', frames, fps=30)
    print("Saved!")

if __name__ == "__main__":
    visualize_and_save()
