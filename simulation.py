import numpy as np

class ProjectileSimulation:
    def __init__(self, gravity=9.81):
        self.g = gravity

    def simulate(self, v0, angle_deg):
        """
        Simulates the projectile motion.

        Args:
            v0 (float): Initial velocity (m/s).
            angle_deg (float): Launch angle in degrees.

        Returns:
            landing_x (float): The x-coordinate where the projectile lands (y=0).
            trajectory (list of tuple): List of (x, y) coordinates.
        """
        angle_rad = np.radians(angle_deg)

        # Calculate total flight time
        # y(t) = v0 * sin(theta) * t - 0.5 * g * t^2 = 0
        # t * (v0 * sin(theta) - 0.5 * g * t) = 0

        if self.g == 0:
            raise ValueError("Gravity cannot be zero.")

        # Avoid division by zero if v0 is 0, t_flight is 0
        if v0 == 0:
            t_flight = 0.0
        else:
            t_flight = (2 * v0 * np.sin(angle_rad)) / self.g

        # Generate trajectory points
        if t_flight == 0:
            trajectory = [(0.0, 0.0)]
            landing_x = 0.0
        else:
            t = np.linspace(0, t_flight, num=100)
            x = v0 * np.cos(angle_rad) * t
            y = v0 * np.sin(angle_rad) * t - 0.5 * self.g * t**2

            # Ensure last point is exactly at y=0
            y[-1] = 0.0

            trajectory = list(zip(x, y))
            landing_x = x[-1]

        return landing_x, trajectory
