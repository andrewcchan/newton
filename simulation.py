import numpy as np

class Simulation:
    def __init__(self, target):
        self.target = target

    def run(self, velocity, angle, gravity):
        angle_rad = np.deg2rad(angle)

        t_flight = 2 * velocity * np.sin(angle_rad) / gravity
        t = np.linspace(0, t_flight, num=100)

        x = velocity * np.cos(angle_rad) * t
        y = velocity * np.sin(angle_rad) * t - 0.5 * gravity * t**2

        hit = self.check_collision(x, y)

        return {
            "x": x.tolist(),
            "y": y.tolist(),
            "hit": hit,
            "target": self.target
        }

    def check_collision(self, x, y):
        for i in range(len(x)):
            dist = np.sqrt((x[i] - self.target["x"])**2 + (y[i] - self.target["y"])**2)
            if dist <= self.target["radius"]:
                return True
        return False
