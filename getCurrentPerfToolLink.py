
#!/usr/bin/env python3
"""Generate a Benchmark Monitor link with up-to-date comparison timestamps.

Comparison modes:
  week-vs-month : last 7 days (B2) compared against the 30 days before them (B1)
  month-vs-year : last 30 days (B2) compared against the 365 days before them (B1)
"""

import argparse
from datetime import datetime, timedelta

BASE_URL = "http://bmdb.me.sap.corp:8089/BM/"

BRANCHES = {
    "fuzzy": "16",
    "orange-fuzzy": "525",
}

DEFAULT_BRANCH = "fuzzy"

BASE_PARAMS = [
    ("_wi", "summary"),
    ("ECFG_COMPILE_TIME", "DEFAULT"),
    ("ICFG_RUN_TIME", "regression%2CtestOnDedicatedSocket"),
    ("EHOST_POOL", "ccde1gl0730"),
    ("EHDB_MAKE_PURPOSE", "CONT"),
    ("EHDB_MAKE_TYPE", "rel"),
    ("IMEASUREMENT_UNIT_ID", "3%2C4"),
]

MODES = {
    "week-vs-month": (7, 30),
    "month-vs-year": (30, 365),
}

TS_FORMAT = "%Y%m%d%H%M%S"


def _range(start: datetime, end: datetime) -> str:
    return f"{start.strftime(TS_FORMAT)},{end.strftime(TS_FORMAT)}"


def build_link(mode: str, branch: str, now: datetime) -> str:
    recent_days, baseline_days = MODES[mode]

    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    recent_start = midnight - timedelta(days=recent_days)
    baseline_end = recent_start - timedelta(seconds=1)
    baseline_start = recent_start - timedelta(days=baseline_days)

    params = [("EHDB_BRANCH_ID", BRANCHES[branch])] + BASE_PARAMS + [
        ("B1TEST_SCRIPT_RUN_TS", _range(baseline_start, baseline_end)),
        ("B2TEST_SCRIPT_RUN_TS", _range(recent_start, now)),
    ]
    return BASE_URL + "?" + "&".join(f"{key}={value}" for key, value in params)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--mode",
        choices=sorted(MODES),
        default="week-vs-month",
        help="comparison period (default: week-vs-month)",
    )
    parser.add_argument(
        "--branch",
        choices=sorted(BRANCHES),
        default=DEFAULT_BRANCH,
        help=f"branch to query (default: {DEFAULT_BRANCH})",
    )
    args = parser.parse_args()
    print(build_link(args.mode, args.branch, datetime.now()))


if __name__ == "__main__":
    main()