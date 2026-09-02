"""
Backtest Runner
===============
Loads OHLC data from a CSV, finds swing pivots, runs the Gann signal
engine, and reports a simple win-rate — so claims about "accuracy" are
backed by numbers on YOUR data, not assumptions.

Usage:
    python backtest.py --csv data/your_data.csv

CSV format expected (header row required):
    timestamp,open,high,low,close
    2024-01-01 09:15,100.0,101.5,99.8,101.0
    ...
"""

import argparse
import csv
from datetime import datetime

from gann.signals import Bar, generate_signals
from gann.angles import calibrate_price_unit


def load_csv(path: str) -> list[Bar]:
    bars = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            bars.append(Bar(
                index=i,
                timestamp=datetime.fromisoformat(row["timestamp"]),
                open=float(row["open"]),
                high=float(row["high"]),
                low=float(row["low"]),
                close=float(row["close"]),
            ))
    return bars


def find_pivots(bars: list[Bar], lookback: int = 10):
    """Very simple pivot finder: local max/min over a window, both sides."""
    pivot_highs, pivot_lows = [], []
    for i in range(lookback, len(bars) - lookback):
        window = bars[i - lookback: i + lookback + 1]
        if bars[i].high == max(b.high for b in window):
            pivot_highs.append(bars[i])
        if bars[i].low == min(b.low for b in window):
            pivot_lows.append(bars[i])
    return pivot_highs, pivot_lows


def evaluate(bars: list[Bar], signals, hold_bars: int = 10):
    """Naive forward-return check: was price higher/lower N bars later?"""
    wins, total = 0, 0
    for sig in signals:
        exit_idx = sig.bar_index + hold_bars
        if exit_idx >= len(bars):
            continue
        entry_price = bars[sig.bar_index].close
        exit_price = bars[exit_idx].close
        correct = (exit_price > entry_price) if sig.direction == "long" else (exit_price < entry_price)
        wins += int(correct)
        total += 1
    return wins, total


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True, help="Path to OHLC CSV file")
    parser.add_argument("--lookback", type=int, default=10, help="Pivot lookback bars")
    parser.add_argument("--hold", type=int, default=10, help="Bars to hold before evaluating a signal")
    args = parser.parse_args()

    bars = load_csv(args.csv)
    if len(bars) < args.lookback * 2 + 5:
        raise SystemExit("Not enough bars for the given lookback.")

    pivot_highs, pivot_lows = find_pivots(bars, args.lookback)
    if not pivot_highs or not pivot_lows:
        raise SystemExit("No pivots found — try a smaller --lookback.")

    last_ph = pivot_highs[-1]
    last_pl = pivot_lows[-1]

    price_range = max(b.high for b in bars) - min(b.low for b in bars)
    price_unit = calibrate_price_unit(price_range, len(bars))

    signals = generate_signals(
        bars,
        pivot_low_idx=last_pl.index, pivot_low_price=last_pl.low,
        pivot_high_idx=last_ph.index, pivot_high_price=last_ph.high,
        price_unit=price_unit,
    )

    wins, total = evaluate(bars, signals, hold_bars=args.hold)

    print(f"Bars loaded:        {len(bars)}")
    print(f"Pivots found:       {len(pivot_highs)} highs, {len(pivot_lows)} lows")
    print(f"Calibrated priceUnit: {price_unit:.6f}")
    print(f"Signals generated:  {len(signals)}")
    if total:
        print(f"Forward win-rate ({args.hold}-bar hold): {wins}/{total} = {wins/total*100:.1f}%")
    else:
        print("No signals had enough forward bars to evaluate.")

    print("\nSample signals:")
    for sig in signals[:10]:
        print(f"  bar {sig.bar_index} | {sig.direction.upper()} ({sig.strength}) | {', '.join(sig.reasons)}")


if __name__ == "__main__":
    main()
