"""
Gann Planetary Longitudes (OPTIONAL — real astronomy, not fake data)
=====================================================================
This is the piece that CANNOT run inside TradingView Pine Script,
because Pine has no orbital-mechanics engine. In Python it CAN be done
for real, using the `skyfield` library (NASA JPL ephemeris data),
because it's deterministic physics — not a live feed you need to
subscribe to.

Install:
    pip install skyfield

Skyfield downloads a small ephemeris file (de421.bsp, ~17MB) on first
run — this requires an internet connection once. After that it works
fully offline.

If skyfield is not installed, every function below raises a clear
ImportError telling you what to install, instead of silently
returning fake numbers.
"""

from datetime import datetime

try:
    from skyfield.api import load
    _SKYFIELD_AVAILABLE = True
except ImportError:
    _SKYFIELD_AVAILABLE = False

PLANETS = ["mercury", "venus", "mars", "jupiter barycenter", "saturn barycenter"]


def _require_skyfield():
    if not _SKYFIELD_AVAILABLE:
        raise ImportError(
            "skyfield is not installed. Run: pip install skyfield\n"
            "This module needs it for real planetary position data — "
            "there is no fallback, because a fake number here would be "
            "misleading rather than helpful."
        )


def geocentric_longitude(dt: datetime, planet: str = "mercury") -> float:
    """
    Real ecliptic longitude (degrees, 0-360) of a planet as seen from
    Earth at the given datetime, using NASA JPL ephemeris data.
    """
    _require_skyfield()
    ts = load.timescale()
    eph = load("de421.bsp")
    earth = eph["earth"]
    body = eph[planet]

    t = ts.utc(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
    astrometric = earth.at(t).observe(body)
    _, lon, _ = astrometric.ecliptic_latlon()
    return lon.degrees % 360


def all_planet_longitudes(dt: datetime) -> dict:
    """Longitudes for all tracked planets at once (one ephemeris load)."""
    _require_skyfield()
    ts = load.timescale()
    eph = load("de421.bsp")
    earth = eph["earth"]
    t = ts.utc(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)

    result = {}
    for planet in PLANETS:
        body = eph[planet]
        astrometric = earth.at(t).observe(body)
        _, lon, _ = astrometric.ecliptic_latlon()
        result[planet] = round(lon.degrees % 360, 2)
    return result
