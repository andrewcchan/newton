import math

class Simulation:
    def __init__(self, g=9.81):
        self.g = g

    def calculate_trajectory(self, v0, angle_degrees, dt=0.1):
        """
        Calculates the trajectory of a projectile.

        Args:
            v0 (float): Initial velocity in m/s.
            angle_degrees (float): Launch angle in degrees.
            dt (float): Time step in seconds.

        Returns:
            list: A list of dictionaries containing 't', 'x', and 'y'.
        """
        angle_rad = math.radians(angle_degrees)
        vx = v0 * math.cos(angle_rad)
        vy_initial = v0 * math.sin(angle_rad)

        trajectory = []
        t = 0.0

        while True:
            x = vx * t
            y = vy_initial * t - 0.5 * self.g * t**2

            if y < 0:
                break

            trajectory.append({
                't': round(t, 2),
                'x': round(x, 2),
                'y': round(y, 2)
            })

            t += dt

        return trajectory
