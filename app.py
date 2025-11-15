from flask import Flask, render_template, jsonify, request
from simulation import Simulation
import random

app = Flask(__name__)

# Define target properties
TARGET = {
    "x": 40,
    "y": 10,
    "radius": 2
}

simulation_env = Simulation(TARGET)

@app.route('/')
def index():
    return render_template('index.html')

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

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
