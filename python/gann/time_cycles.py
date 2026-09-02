"""
Gann Time Cycles
================
Gann's recurring "natural" numbers, referenced throughout his books
(45 Years in Wall Street, Truth of the Tape). These are bar/day counts
from a major pivot where reversals were historically more likely.

NOTE: Gann's original master cycles (60-year, 82-year) were built from
decades of hand-tracked, market-specific historical data he never fully
published. The numbers below are his commonly cited SHORT cycles, not
the master cycle itself.
"""

DEFAULT_CYCLES = [45, 90, 120, 144, 180, 270, 360]

MASTER_CYCLE_CANDIDATES = [60, 82]  # bars/years, market-dependent, unverified origin


def project_cycles(pivot_index: int, cycles: list[int] | None = None) -> list[int]:
    """Return bar indices where each cycle lands, counted from pivot_index."""
    cycles = cycles or DEFAULT_CYCLES
    return [pivot_index + c for c in cycles]


def nearest_cycle_hit(bar_index: int, pivot_index: int, cycles: list[int] | None = None,
                       tolerance: int = 1) -> int | None:
    """Check if bar_index falls on (within tolerance of) a projected cycle."""
    cycles = cycles or DEFAULT_CYCLES
    elapsed = bar_index - pivot_index
    for c in cycles:
        if abs(elapsed - c) <= tolerance:
            return c
    return None
