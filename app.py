from flask import Flask, render_template, request, jsonify
from simulation import Simulation

app = Flask(__name__)
simulation = Simulation()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/simulate', methods=['POST'])
def simulate():
    data = request.json
    try:
        v0 = float(data.get('v0'))
        angle = float(data.get('angle'))

        # Validate inputs
        if v0 < 0:
            return jsonify({'error': 'Velocity must be non-negative'}), 400
        if not (0 <= angle <= 90):
            return jsonify({'error': 'Angle must be between 0 and 90 degrees'}), 400

        trajectory = simulation.calculate_trajectory(v0, angle)
        return jsonify({'trajectory': trajectory})

    except (TypeError, ValueError):
        return jsonify({'error': 'Invalid input values'}), 400

if __name__ == '__main__':
    app.run(debug=True)
