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

    # Calculate angle vector for visualization
    max_range = np.max(x) if len(x) > 0 else 1
    vector_len = max_range * 0.1 # 10% of the max range
    angle_vector_x = [0, vector_len * np.cos(angle_rad)]
    angle_vector_y = [0, vector_len * np.sin(angle_rad)]

    return jsonify({
        't': t.tolist(),
        'x': x.tolist(),
        'y': y.tolist(),
        'vx_t': vx_t.tolist(),
        'vy_t': vy_t.tolist(),
        'angle_vector': {
            'x': angle_vector_x,
            'y': angle_vector_y
        }
    })

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
