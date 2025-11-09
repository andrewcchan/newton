from flask import Flask, render_template, jsonify, request
import numpy as np
import random

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# Define target properties
TARGET = {
    "x": 40,
    "y": 10,
    "radius": 2
}

@app.route('/simulate', methods=['POST'])
def simulate():
    velocity = float(request.json['velocity'])
    angle = np.deg2rad(float(request.json['angle']))
    gravity = float(request.json['gravity'])

    t_flight = 2 * velocity * np.sin(angle) / gravity
    t = np.linspace(0, t_flight, num=100)

    x = velocity * np.cos(angle) * t
    y = velocity * np.sin(angle) * t - 0.5 * gravity * t**2

    # Check for collision with the target
    hit = False
    for i in range(len(x)):
        dist = np.sqrt((x[i] - TARGET["x"])**2 + (y[i] - TARGET["y"])**2)
        if dist <= TARGET["radius"]:
            hit = True
            break

    return jsonify(
        x=x.tolist(),
        y=y.tolist(),
        hit=hit,
        target=TARGET
    )

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)