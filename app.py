from flask import Flask, render_template, request, jsonify
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    velocity = float(data['velocity'])
    angle = float(data['angle'])

    g = 9.81
    angle_rad = np.deg2rad(angle)
    v_x = velocity * np.cos(angle_rad)
    v_y = velocity * np.sin(angle_rad)
    t_flight = (2 * v_y) / g
    t = np.linspace(0, t_flight, num=100)
    x = v_x * t
    y = v_y * t - 0.5 * g * t**2

    vx_t = np.full_like(t, v_x)
    vy_t = v_y - g * t

    return jsonify({
        't': t.tolist(),
        'x': x.tolist(),
        'y': y.tolist(),
        'vx_t': vx_t.tolist(),
        'vy_t': vy_t.tolist()
    })

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
