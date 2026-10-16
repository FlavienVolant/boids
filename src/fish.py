from typing import Tuple

class Fish:
    __slots__ = ("pos_x", "pos_y", "vel_x", "vel_y")

    def __init__(self, position: Tuple[float, float] = (0, 0), velocity: Tuple[float, float] = (0, 0)):
        self.pos_x, self.pos_y = position
        self.vel_x, self.vel_y = velocity

    def update(self, dt: float) -> None:
        self.pos_x += self.vel_x * dt
        self.pos_y += self.vel_y * dt

    @property
    def position(self):
        return self.pos_x, self.pos_y

    @property
    def velocity(self):
        return self.vel_x, self.vel_y