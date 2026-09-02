"""
Gann Percentage Retracements
=============================
Gann's own retracement ratios — eighths (1/8 steps) plus the key
thirds (1/3, 2/3). Distinct from Fibonacci, though 50% and 62.5%/37.5%
happen to land close to Fibonacci's 50%/61.8%/38.2%.
"""

GANN_RATIOS = [1 / 8, 1 / 4, 1 / 3, 3 / 8, 1 / 2, 5 / 8, 2 / 3, 3 / 4, 7 / 8]


def retracement_levels(swing_high: float, swing_low: float) -> dict[str, float]:
    """Return a dict of {percentage_label: price_level} between a swing high/low."""
    price_range = swing_high - swing_low
    levels = {}
    for r in GANN_RATIOS:
        label = f"{round(r * 100, 1)}%"
        levels[label] = round(swing_high - price_range * r, 4)
    return levels
