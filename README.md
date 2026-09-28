# getCurrentPerfToolLink

Generates a Benchmark Monitor (BMDB) summary link with up-to-date comparison
timestamps, so you no longer have to edit the date ranges in the URL by hand.

## Usage

```bash
python3 getCurrentPerfToolLink.py [--mode MODE] [--branch BRANCH]
```

The generated URL is printed to stdout; paste it into a browser.

### Options

| Option     | Values                         | Default         | Description                                |
| ---------- | ------------------------------ | --------------- | ------------------------------------------ |
| `--mode`   | `week-vs-month`, `month-vs-year` | `week-vs-month` | Which time periods to compare              |
| `--branch` | `fuzzy`, `orange-fuzzy`        | `fuzzy`         | Branch whose measurements are queried      |

### Comparison modes

Both windows are adjacent and non-overlapping. The recent window (`B2`) ends at
the current time; the baseline window (`B1`) ends one second before the recent
window starts.

- `week-vs-month`: last 7 days compared against the 30 days before them.
- `month-vs-year`: last 30 days compared against the 365 days before them.

### Branches

| Name           | `EHDB_BRANCH_ID` |
| -------------- | ---------------- |
| `fuzzy`        | 16               |
| `orange-fuzzy` | 525              |

## Examples

```bash
# Default: last week vs. the preceding month on branch 'fuzzy'
python3 getCurrentPerfToolLink.py

# Last month vs. the preceding year on branch 'orange-fuzzy'
python3 getCurrentPerfToolLink.py --mode month-vs-year --branch orange-fuzzy
```

## Customizing

The fixed query parameters (host pool, make type, run-time configuration,
measurement units, ...) live in `BASE_PARAMS` in `getCurrentPerfToolLink.py`.
Additional branches can be added to the `BRANCHES` map, additional comparison
windows to the `MODES` map.

## Requirements

Python 3 (standard library only).
