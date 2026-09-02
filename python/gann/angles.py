"""
Gann Angle Fan
==============
Projects Gann's classic angle ratios (1x1, 2x1, 4x1, 1x2, 1x4) forward
in time from a chosen pivot (swing high or swing low).

price_unit: how much price moves per 1 bar on the 1x1 (45-degree) angle.
This MUST be calibrated per instrument/timeframe — Gann himself adjusted
this per market. A wrong price_unit makes every angle meaningless.
"""

from dataclasses import dataclass

# Gann's classic angle ratios: (price_multiplier, label)
GANN_RATIOS = {
    "1x8": 1 / 8,
    "1x4": 1 / 4,
    "1x3": 1 / 3,
    "1x2": 1 / 2,
    "1x1": 1.0,
    "2x1": 2.0,
    "3x1": 3.0,
    "4x1": 4.0,
    "8x1": 8.0,
}


@dataclass
class GannAngle:
    ratio_name: str
    pivot_bar: int
    pivot_price: float
    price_unit: float
    direction: int  # +1 = up angle (from a low), -1 = down angle (from a high)

    def value_at(self, bar_index: int) -> float:
        """Projected price of this angle at a given bar index."""
        multiplier = GANN_RATIOS[self.ratio_name]
        bars_elapsed = bar_index - self.pivot_bar
        return self.pivot_price + self.direction * bars_elapsed * self.price_unit * multiplier


def build_fan(pivot_bar: int, pivot_price: float, price_unit: float, direction: int,
              ratios=("1x4", "1x2", "1x1", "2x1", "4x1")):
    """Build a full fan of GannAngle objects from one pivot."""
    return [GannAngle(r, pivot_bar, pivot_price, price_unit, direction) for r in ratios]


def calibrate_price_unit(price_range: float, bar_range: int) -> float:
    """
    Suggests a starting price_unit so the 1x1 angle visually spans the
    given price_range over the given bar_range (i.e. true 45 degrees on
    a chart where that range fills the visible window equally).
    """
    if bar_range <= 0:
        raise ValueError("bar_range must be > 0")
    return price_range / bar_range
