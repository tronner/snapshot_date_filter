#!/usr/bin/env python3
import sys
from datetime import datetime, timedelta, timezone
import snapshot_date_filter as sdf

now = datetime(year=2020, month=12, day=30, hour=0, minute=0)
input_dates = []
fmt = "data/datastore1@auto-%Y-%m-%d_%H.%M"
reten = {
    "hour": 24,
    "day": 7,
    "week": 4,
    "4week": 13
}
now = datetime(year=2020, month=12, day=30, hour=0, minute=0)
i = 0
while True:
    i += 1
    sys.stderr.write(f"RUN {i:02}  NOW {now.strftime('%Y-%m-%d_%H.%M.%S')}\n")
    output_dates = sdf.date_filter(True, input_dates, reten, keep_latest=True, now=now, keep_younger=True)
    output_names = [outdate.strftime(fmt) for outdate in output_dates]
    print("\n".join(output_names))
    #input()
    print()
    now += timedelta(seconds=300)
    output_dates.append(now)
    input_dates = output_dates
