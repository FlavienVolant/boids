
import math

def normalize(vector: tuple[float, float]) -> tuple[float, float]:
    x, y = vector
    magnitude = math.hypot(x, y)
    if magnitude == 0.0:
        return 0.0, 0.0
    return x / magnitude, y / magnitude

def toroidal_offset(origin: tuple[float, float], target: tuple[float, float], width: float, height: float) -> tuple[float, float]:
    dx = target[0] - origin[0]
    dy = target[1] - origin[1]

    if dx > width / 2:
        dx -= width
    elif dx < -width / 2:
        dx += width

    if dy > height / 2:
        dy -= height
    elif dy < -height / 2:
        dy += height

    return dx, dy
