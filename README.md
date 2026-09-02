# Gann Trading System

W.D. Gann's published technical concepts implemented two ways:
1. A live **TradingView Pine Script v6 indicator** (chart overlay, signals, alerts)
2. A **Python research/backtest package** (same concepts, testable on your own historical data)

## Folder structure

```
gann-trading-system/
├── indicators/
│   └── pine/
│       └── gann_advanced_system.pine      <- paste into TradingView Pine Editor
├── python/
│   ├── gann/                              <- reusable Gann math package
│   │   ├── __init__.py
│   │   ├── angles.py                      <- Gann angle fan (1x1, 2x1, 4x1, 1x2, 1x4)
│   │   ├── square_of_nine.py              <- Cardinal / Ordinal price levels
│   │   ├── time_cycles.py                 <- 45/90/120/144/180/270/360 bar cycles
│   │   ├── retracements.py                <- Gann's % retracement ratios
│   │   ├── lunar.py                       <- real moon-phase math (new/full moon)
│   │   ├── planetary.py                   <- OPTIONAL real planetary longitudes (needs skyfield)
│   │   └── signals.py                     <- combines everything into entry/exit signals
│   ├── backtest.py                        <- run this: python backtest.py --csv data/your_data.csv
│   ├── requirements.txt
│   └── data/                              <- put your own OHLC CSV files here
├── docs/
│   └── gann_concepts.md                   <- what each concept is and its source book
├── LICENSE
├── .gitignore
└── README.md
```

## Quick start — Pine Script (TradingView)

1. Open TradingView → Pine Editor
2. Paste the contents of `indicators/pine/gann_advanced_system.pine`
3. Click "Add to Chart"
4. Calibrate `Gann Price Unit` in the settings so the 1x1 angle line visually
   sits at ~45 degrees on your chart — this step is mandatory, skipping it
   makes every angle-based signal meaningless.

## Quick start — Python backtest

```bash
cd python
pip install -r requirements.txt     # only needed if you want the optional planetary module
python backtest.py --csv data/your_data.csv --lookback 10 --hold 10
```

CSV format required (header row):
```
timestamp,open,high,low,close
2024-01-01 09:15,100.0,101.5,99.8,101.0
```

## What's real vs. what's a documented limitation

| Concept | Status |
|---|---|
| Gann Angle Fan | ✅ Real geometry, calibration-dependent |
| Square of Nine (Cardinal/Ordinal) | ✅ Real formula from his spiral chart |
| Time Cycles (45/90/120/144/180/270/360) | ✅ Gann's documented numbers |
| Percentage Retracements | ✅ Gann's own ratios (not Fibonacci) |
| Rule of Thumb (count-based OB/OS) | ✅ From *45 Years in Wall Street* |
| Lunar Cycle (new/full moon) | ✅ Real synodic-month astronomy, pure math |
| Planetary longitudes | ✅ Real (Python + skyfield/NASA ephemeris), ❌ not possible in Pine Script |
| Master 60/82-year cycle (his original) | ⚠️ Simplified analogue only — his original dataset was never fully published |
| Gann's exact discretionary trading rules | ⚠️ Not fully code-able — he applied personal judgment on top of these tools |

See `docs/gann_concepts.md` for source-book references for each concept.

## Disclaimer

This is an educational/research implementation of publicly documented technical
analysis concepts. It is not financial advice, and no historical win-rate here
is a guarantee of future performance. Backtest thoroughly on your own data
before risking real capital.
