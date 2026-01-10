from flask import Flask, render_template, jsonify, request
from simulation import Simulation
from rl_agent import RLAgent
import numpy as np
import random

app = Flask(__name__)

# Define target properties
TARGET = {
    "x": 40,
    "y": 10,
    "radius": 2
}

simulation_env = Simulation(TARGET)

# --- RL Agent Setup ---
agent = RLAgent(simulation_env)
ai_enabled = False
try:
    agent.q_table = np.load("q_table.npy", allow_pickle=True)
    agent.epsilon = 0.0 # pure exploitation
    ai_enabled = True
    print("--- Q-table loaded successfully. ---")
except FileNotFoundError:
    print("--- WARNING: q_table.npy not found. The agent is not trained. ---")
    # Handle the case where the Q-table doesn't exist, maybe disable the AI feature?
    # For now, the agent will be untrained.
    pass

@app.route('/')
def index():
    return render_template('index.html', ai_enabled=ai_enabled)

@app.route('/simulate', methods=['POST'])
def simulate():
    try:
        velocity = float(request.json['velocity'])
        angle = float(request.json['angle'])
        gravity = float(request.json['gravity'])

        if velocity <= 0 or angle < 0 or angle > 90 or gravity < 0:
            raise ValueError("Invalid simulation parameters.")

        result = simulation_env.run(velocity, angle, gravity)
        return jsonify(result)

    except (KeyError, ValueError) as e:
        return jsonify({"error": str(e)}), 400

@app.route('/solve', methods=['POST'])
def solve():
    if not ai_enabled:
        return jsonify({"error": "AI feature is currently unavailable"}), 400

    try:
        gravity = float(request.json['gravity'])
        if gravity < 0:
            raise ValueError("Invalid gravity value.")

        # Use the agent to find the best action
        state = agent.get_state(gravity)
        action = agent.choose_action(state)
        velocity, angle = agent.get_action_values(action)

        # Run the simulation with the agent's chosen parameters
        result = simulation_env.run(velocity, angle, gravity)
        return jsonify(result)

    except (KeyError, ValueError) as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
