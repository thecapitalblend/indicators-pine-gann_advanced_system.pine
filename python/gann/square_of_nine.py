"""
Square of Nine
==============
Gann's spiral number grid. Numbers are arranged in a clockwise (or
counter-clockwise) spiral starting from 1 at the center. Angular
"spokes" from the center land on specific numbers:

    Cardinal spokes (0/90/180/270 degrees)  -> whole-step increments of sqrt(base)
    Ordinal spokes  (45/135/225/315 degrees) -> half-step increments of sqrt(base)

These become horizontal support/resistance price levels once you take
sqrt(base_price), step it, and square it back.
"""

import math


def cardinal_levels(base_price: float, steps: int = 4) -> list[float]:
    """Whole-step (90-degree spoke) levels around base_price."""
    r = math.sqrt(base_price)
    return [round((r + i) ** 2, 4) for i in range(-steps, steps + 1)]


def ordinal_levels(base_price: float, steps: int = 4) -> list[float]:
    """Half-step (45-degree spoke) levels around base_price."""
    r = math.sqrt(base_price)
    return [round((r + i * 0.5) ** 2, 4) for i in range(-steps, steps + 1)]


def nearest_level(price: float, levels: list[float]) -> float:
    """Find the closest Square-of-Nine level to a given price."""
    return min(levels, key=lambda lvl: abs(lvl - price))


def square_of_nine_grid(size: int = 9) -> list[list[int]]:
    """
    Build the literal spiral number grid (size x size, odd number),
    useful for visualising Gann's original hand-drawn chart.
    """
    if size % 2 == 0:
        raise ValueError("size must be odd")
    grid = [[0] * size for _ in range(size)]
    center = size // 2
    x = y = center
    grid[y][x] = 1
    num = 2
    step = 1
    dirs = [(1, 0), (0, -1), (-1, 0), (0, 1)]  # right, up, left, down
    d = 0
    while num <= size * size:
        for _ in range(2):
            dx, dy = dirs[d % 4]
            for _ in range(step):
                if num > size * size:
                    break
                x += dx
                y += dy
                if 0 <= x < size and 0 <= y < size:
                    grid[y][x] = num
                    num += 1
            d += 1
        step += 1
    return grid
