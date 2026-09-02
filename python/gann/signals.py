"""
Signal Engine
=============
Combines angles, Square of Nine, time cycles, retracements, and the
lunar cycle into a single scored signal per bar. This mirrors the
Pine Script indicator's logic so results are comparable.
"""

from dataclasses import dataclass, field
from datetime import datetime

from .angles import build_fan
from .time_cycles import nearest_cycle_hit
from .lunar import is_new_moon, is_full_moon


@dataclass
class Bar:
    index: int
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float


@dataclass
class Signal:
    bar_index: int
    direction: str  # "long" / "short"
    strength: str   # "normal" / "strong"
    reasons: list = field(default_factory=list)


def generate_signals(bars: list[Bar], pivot_low_idx: int, pivot_low_price: float,
                      pivot_high_idx: int, pivot_high_price: float,
                      price_unit: float, require_confluence: bool = True) -> list[Signal]:
    """
    Walk through bars and flag Gann angle crossovers, same as the
    Pine Script version (1x1 base signal, 2x1 confluence = strong).
    """
    up_fan = build_fan(pivot_low_idx, pivot_low_price, price_unit, direction=1)
    down_fan = build_fan(pivot_high_idx, pivot_high_price, price_unit, direction=-1)

    up_1x1 = next(a for a in up_fan if a.ratio_name == "1x1")
    up_2x1 = next(a for a in up_fan if a.ratio_name == "2x1")
    dn_1x1 = next(a for a in down_fan if a.ratio_name == "1x1")
    dn_2x1 = next(a for a in down_fan if a.ratio_name == "2x1")

    signals = []
    for i in range(1, len(bars)):
        prev, cur = bars[i - 1], bars[i]

        up_val_prev, up_val_cur = up_1x1.value_at(prev.index), up_1x1.value_at(cur.index)
        dn_val_prev, dn_val_cur = dn_1x1.value_at(prev.index), dn_1x1.value_at(cur.index)

        crossed_up = prev.close <= up_val_prev and cur.close > up_val_cur
        crossed_down = prev.close >= dn_val_prev and cur.close < dn_val_cur

        if crossed_up:
            reasons = ["1x1 angle crossover (up)"]
            strong = require_confluence and cur.close > up_2x1.value_at(cur.index)
            if strong:
                reasons.append("2x1 confluence")

            cycle_hit = nearest_cycle_hit(cur.index, pivot_low_idx)
            if cycle_hit:
                reasons.append(f"Gann time cycle {cycle_hit} bars")
            if is_new_moon(cur.timestamp):
                reasons.append("New moon window")

            signals.append(Signal(cur.index, "long", "strong" if strong else "normal", reasons))

        if crossed_down:
            reasons = ["1x1 angle crossover (down)"]
            strong = require_confluence and cur.close < dn_2x1.value_at(cur.index)
            if strong:
                reasons.append("2x1 confluence")

            cycle_hit = nearest_cycle_hit(cur.index, pivot_high_idx)
            if cycle_hit:
                reasons.append(f"Gann time cycle {cycle_hit} bars")
            if is_full_moon(cur.timestamp):
                reasons.append("Full moon window")

            signals.append(Signal(cur.index, "short", "strong" if strong else "normal", reasons))

    return signals
