import pygame

from fish import Fish
from utils import toroidal_offset

FISH_SIZE = 5
FISH_COLOR = "yellow"

SEPARATION_RADIUS = 25.0
ALIGNMENT_RADIUS = 65.0
COHESION_RADIUS = 90.0

SEPARATION_WEIGHT = 0.5
ALIGNMENT_WEIGHT = 0.6
COHESION_WEIGHT = 0.45

class Simulation:
    __slots__ = ("fishs")

    def __init__(self, fishs: list[Fish]):
        self.fishs = fishs

    def get_neighbors(self, fish: Fish, radius: float, width: float, height: float) -> list[Fish]:
        radius_sq = radius * radius
        result = []

        for other in self.fishs:
            if other is fish:
                continue
            dx, dy = toroidal_offset(fish.position, other.position, width, height)
            if dx * dx + dy * dy < radius_sq:
                result.append(other)

        return result

    def update(self, dt: float, max_x: float, max_y: float) -> None:

        directions = []

        for fish in self.fishs:

            separation = fish.separation(
                self.get_neighbors(fish, SEPARATION_RADIUS, max_x, max_y),
                max_x,
                max_y,
            )
            alignment = fish.alignment(
                self.get_neighbors(fish, ALIGNMENT_RADIUS, max_x, max_y)
            )
            cohesion = fish.cohesion(
                self.get_neighbors(fish, COHESION_RADIUS, max_x, max_y),
                max_x,
                max_y,
            )

            direction_x = (
                separation[0] * SEPARATION_WEIGHT
                + alignment[0] * ALIGNMENT_WEIGHT
                + cohesion[0] * COHESION_WEIGHT
            )

            direction_y = (
                separation[1] * SEPARATION_WEIGHT
                + alignment[1] * ALIGNMENT_WEIGHT
                + cohesion[1] * COHESION_WEIGHT
            )

            directions.append((direction_x, direction_y))

        for fish, direction in zip(self.fishs, directions):
            fish.update(dt, max_x, max_y, direction)

    def draw(self, screen) -> None:
        for fish in self.fishs:
            pygame.draw.circle(screen, FISH_COLOR, fish.position, FISH_SIZE)