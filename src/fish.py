import math
import random
from typing import Self, Tuple

from utils import normalize, toroidal_offset

MAX_STEERING = 60.0
MIN_SPEED = 70.0
MAX_SPEED = 150.0

class Fish:
    __slots__ = (
        "pos_x", "pos_y",
        "vel_x", "vel_y", 
        "acc_x", "acc_y",
        "target_speed"
    )

    def __init__(self, 
                 target_speed: float = random.uniform(MIN_SPEED, MAX_SPEED),
                 position: Tuple[float, float] = (0, 0), 
                 velocity: Tuple[float, float] = (0, 0),
        ):
        self.target_speed = target_speed
        self.pos_x, self.pos_y = position

        speed = math.hypot(*velocity)
        if speed == 0.0:
            angle = random.uniform(0.0, 2.0 * math.pi)
            self.vel_x = math.cos(angle) * self.target_speed
            self.vel_y = math.sin(angle) * self.target_speed
        else:
            self.vel_x = velocity[0] * self.target_speed / speed
            self.vel_y = velocity[1] * self.target_speed / speed

    @property
    def position(self):
        return self.pos_x, self.pos_y
    
    @property
    def velocity(self):
        return self.vel_x, self.vel_y

    def apply_acceleration(self, force: Tuple[float, float]) -> None:
        self.acc_x += force[0]
        self.acc_y += force[1]

    def separation(self, neighbors: list[Self], width: float, height: float) -> Tuple[float, float]:
        separation_x = 0.0
        separation_y = 0.0

        for fish in neighbors:
            dx, dy = toroidal_offset(self.position, fish.position, width, height)
            distance_sq = dx * dx + dy * dy
            if distance_sq == 0.0:
                continue

            separation_x -= dx / distance_sq
            separation_y -= dy / distance_sq

        return normalize((separation_x, separation_y))

    def alignment(self, neighbors: list[Self]) -> Tuple[float, float]:

        if not neighbors:
            return 0.0, 0.0

        average_x = sum(fish.vel_x for fish in neighbors) / len(neighbors)
        average_y = sum(fish.vel_y for fish in neighbors) / len(neighbors)

        return normalize((average_x, average_y))

    def cohesion(self, neighbors: list[Self], width: float, height: float) -> Tuple[float, float]:

        if not neighbors:
            return 0.0, 0.0

        offsets = [
            toroidal_offset(self.position, fish.position, width, height)
            for fish in neighbors
        ]

        center_x = sum(dx for dx, _ in offsets) / len(offsets)
        center_y = sum(dy for _, dy in offsets) / len(offsets)

        return normalize((center_x, center_y))

    def change_direction(self, direction: tuple[float, float]) -> None:
        dx, dy = direction

        if dx == 0.0 and dy == 0.0:
            return

        dx, dy = normalize((dx, dy))

        if dx == 0.0 and dy == 0.0:
            return

        self.vel_x = dx * self.target_speed
        self.vel_y = dy * self.target_speed

    def update(self, dt: float, max_x: float, max_y: float, direction: tuple[float, float]) -> None:

        self.change_direction(direction)

        self.pos_x = (self.pos_x + self.vel_x * dt) % max_x
        self.pos_y = (self.pos_y + self.vel_y * dt) % max_y