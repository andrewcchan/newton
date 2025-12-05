import pytest
from simulation import Simulation

def test_simulation_initialization():
    sim = Simulation()
    assert sim.g == 9.81

def test_trajectory_calculation_basic():
    sim = Simulation()
    # Test firing straight up (90 degrees)
    # x should stay 0 (approx), y should go up and down
    trajectory = sim.calculate_trajectory(v0=10, angle_degrees=90)

    assert len(trajectory) > 0
    first_point = trajectory[0]
    assert first_point['t'] == 0.0
    assert first_point['x'] == 0.0
    assert first_point['y'] == 0.0

    # Check that x is always 0
    for point in trajectory:
        assert abs(point['x']) < 1e-10

def test_trajectory_calculation_45_degrees():
    sim = Simulation()
    trajectory = sim.calculate_trajectory(v0=10, angle_degrees=45)

    # Should land eventually (y goes back to near 0 or negative then cut off)
    # The simulation loop breaks when y < 0, but the last point added is before that?
    # No, the code adds point, then increments t.
    # Wait, the loop checks if y < 0 break, so it DOES NOT add the negative point.

    last_point = trajectory[-1]
    assert last_point['y'] >= 0

    # Max range for v=10, ang=45 is v^2/g * sin(2theta) = 100/9.81 * 1 approx 10.19m
    # Let's check if the last x is close to that.
    # Note: since it stops when y<0, the last point might be slightly before the true landing.
    assert 9.0 < last_point['x'] < 11.0

def test_trajectory_empty_input():
    # If velocity is 0, should just return start point or empty?
    sim = Simulation()
    trajectory = sim.calculate_trajectory(v0=0, angle_degrees=45)
    # Loop: t=0 -> x=0, y=0. Append. t+=dt.
    # t=0.1 -> y = -0.5*g*t^2 < 0. Break.
    # So returns one point (0,0,0)
    assert len(trajectory) == 1
    assert trajectory[0]['x'] == 0
    assert trajectory[0]['y'] == 0
