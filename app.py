import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation

st.set_page_config(page_title="Projectile Motion Kinematics")

st.title("Projectile Motion Kinematics")

st.header("Simulation")

velocity = st.slider("Initial Velocity (m/s)", 1, 100, 25)
angle = st.slider("Launch Angle (degrees)", 0, 90, 45)

g = 9.81
angle_rad = np.deg2rad(angle)
v_x = velocity * np.cos(angle_rad)
v_y = velocity * np.sin(angle_rad)
t_flight = (2 * v_y) / g
t = np.linspace(0, t_flight, num=100)
x = v_x * t
y = v_y * t - 0.5 * g * t**2

fig, ax = plt.subplots()
ax.set_xlim(0, np.max(x) * 1.1)
ax.set_ylim(0, np.max(y) * 1.1)
ax.set_xlabel("x (m)")
ax.set_ylabel("y (m)")
ax.set_title("Projectile Trajectory")
line, = ax.plot([], [], 'o-', lw=2)

def update(frame):
    line.set_data(x[:frame], y[:frame])
    return line,

ani = animation.FuncAnimation(fig, update, frames=len(t), blit=True)

# Convert the animation to an HTML5 video.
html_video = ani.to_html5_video()
# Embed the video in the Streamlit app.
components.html(html_video, height=400)


st.header("Kinematic Graphs")

# Calculate velocity components over time
vx_t = np.full_like(t, v_x)
vy_t = v_y - g * t

# Create a 2x2 grid of subplots for the kinematic graphs
fig_kin, axs = plt.subplots(2, 2, figsize=(10, 8))
fig_kin.tight_layout(pad=4.0)

# Position vs. Time plots
line_px, = axs[0, 0].plot([], [], lw=2)
axs[0, 0].set_xlim(0, t_flight)
axs[0, 0].set_ylim(0, np.max(x) * 1.1 if np.max(x) > 0 else 1)
axs[0, 0].set_xlabel("Time (s)")
axs[0, 0].set_ylabel("x Position (m)")
axs[0, 0].set_title("x Position vs. Time")
axs[0, 0].grid(True)


line_py, = axs[0, 1].plot([], [], lw=2)
axs[0, 1].set_xlim(0, t_flight)
axs[0, 1].set_ylim(0, np.max(y) * 1.1 if np.max(y) > 0 else 1)
axs[0, 1].set_xlabel("Time (s)")
axs[0, 1].set_ylabel("y Position (m)")
axs[0, 1].set_title("y Position vs. Time")
axs[0, 1].grid(True)

# Velocity vs. Time plots
line_vx, = axs[1, 0].plot([], [], lw=2)
axs[1, 0].set_xlim(0, t_flight)
axs[1, 0].set_ylim(0, v_x * 1.2 if v_x > 0 else 1)
axs[1, 0].set_xlabel("Time (s)")
axs[1, 0].set_ylabel("x Velocity (m/s)")
axs[1, 0].set_title("x Velocity vs. Time")
axs[1, 0].grid(True)

line_vy, = axs[1, 1].plot([], [], lw=2)
axs[1, 1].set_xlim(0, t_flight)
# Handle y-velocity range which goes from positive to negative
min_vy = np.min(vy_t)
max_vy = np.max(vy_t)
axs[1, 1].set_ylim(min_vy - abs(min_vy * 0.1), max_vy + abs(max_vy * 0.1))
axs[1, 1].set_xlabel("Time (s)")
axs[1, 1].set_ylabel("y Velocity (m/s)")
axs[1, 1].set_title("y Velocity vs. Time")
axs[1, 1].grid(True)

def update_kin(frame):
    # x position
    line_px.set_data(t[:frame], x[:frame])
    # y position
    line_py.set_data(t[:frame], y[:frame])
    # x velocity
    line_vx.set_data(t[:frame], vx_t[:frame])
    # y velocity
    line_vy.set_data(t[:frame], vy_t[:frame])
    return line_px, line_py, line_vx, line_vy,

ani_kin = animation.FuncAnimation(fig_kin, update_kin, frames=len(t), blit=True, interval=20)

# Convert the animation to an HTML5 video.
html_video_kin = ani_kin.to_html5_video()
# Embed the video in the Streamlit app.
components.html(html_video_kin, height=800)

st.header("Equations")

st.markdown(r'''
$$
v_x = v_{0x}
$$
''')

st.markdown(r'''
$$
x = x_0 + v_{0x}t
$$
''')

st.markdown(r'''
$$
v_y = v_{0y} - gt
$$
''')

st.markdown(r'''
$$
y = y_0 + v_{0y}t - \frac{1}{2}gt^2
$$
''')

st.markdown(r'''
$$
v_y^2 = v_{0y}^2 - 2g(y - y_0)
$$
''')
