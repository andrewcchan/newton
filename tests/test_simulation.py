import pytest
from simulation import Simulation
import numpy as np

TARGET = {"x": 40, "y": 10, "radius": 2}

@pytest.fixture
def sim():
    return Simulation(TARGET)

def test_simulation_run(sim):
    """Test that the simulation runs and returns the expected data structure."""
    result = sim.run(velocity=20, angle=45, gravity=9.8)
    assert isinstance(result, dict)
    assert "x" in result and "y" in result and "hit" in result
    assert len(result["x"]) == 100 and len(result["y"]) == 100

def test_collision_detection_hit(sim):
    """
    Test that a hit is correctly detected.
    These parameters were found programmatically to ensure a reliable hit.
    """
    result = sim.run(velocity=22.07, angle=44.60, gravity=9.8)
    assert result["hit"] is True, "The projectile should have hit the target."

def test_collision_detection_miss(sim):
    """Test that a clear miss is correctly detected."""
    result = sim.run(velocity=10, angle=45, gravity=9.8)
    assert result["hit"] is False

def test_zero_gravity(sim):
    """Test that zero gravity results in a straight line with no hit."""
    result = sim.run(velocity=10, angle=45, gravity=0)
    # With zero gravity, y should be a straight, upward-sloping line
    y_coords = np.array(result["y"])
    assert np.all(np.diff(y_coords) > 0)
    assert result["hit"] is False
