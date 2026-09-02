"""
Gann Lunar Cycle (Moon Phase)
=============================
Real astronomical calculation using the Moon's synodic month
(29.530588853 days) — the actual time between consecutive new moons.
No external data feed or API needed; this is deterministic math based
on a known reference new moon.

This matches the identical formula used in the Pine Script indicator,
so results here can be cross-checked against the TradingView chart.
"""

from datetime import datetime, timezone, timedelta

SYNODIC_MONTH_DAYS = 29.530588853
# A well-documented reference new moon (Jan 6, 2000, 18:14 UTC)
KNOWN_NEW_MOON = datetime(2000, 1, 6, 18, 14, tzinfo=timezone.utc)


def moon_phase(dt: datetime) -> float:
    """
    Returns the Moon's phase age in days (0 = new moon,
    ~14.77 = full moon, wraps back to 0 at ~29.53).
    """
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    days_since = (dt - KNOWN_NEW_MOON).total_seconds() / 86400.0
    phase = days_since % SYNODIC_MONTH_DAYS
    return phase


def is_new_moon(dt: datetime, tolerance_days: float = 1.0) -> bool:
    phase = moon_phase(dt)
    return phase <= tolerance_days or phase >= (SYNODIC_MONTH_DAYS - tolerance_days)


def is_full_moon(dt: datetime, tolerance_days: float = 1.0) -> bool:
    phase = moon_phase(dt)
    return abs(phase - SYNODIC_MONTH_DAYS / 2) <= tolerance_days


def next_new_moon(dt: datetime) -> datetime:
    phase = moon_phase(dt)
    days_remaining = SYNODIC_MONTH_DAYS - phase
    return dt + timedelta(days=days_remaining)


def next_full_moon(dt: datetime) -> datetime:
    phase = moon_phase(dt)
    half = SYNODIC_MONTH_DAYS / 2
    days_remaining = (half - phase) if phase < half else (SYNODIC_MONTH_DAYS - phase + half)
    return dt + timedelta(days=days_remaining)
