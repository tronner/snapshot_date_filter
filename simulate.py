#!/usr/bin/env python3
"""simulate.py

Simulate snapshot creation and removal. The initial snapshot list
will be read from stdin.

Most options work like their counterpart in the main program.

Usage:
    simulate.py -f <fmt> -r <reten> -i <interval_seconds> [-c | --create]
                [-l | --keep-latest] [-y | --keep-younger] [-p | --prompt]
    simulate.py (-h | --help | --version | -R | --list-valid-intervals)

Options:
    -h, --help          Show usase
    --version           Show version
    -R, --list-valid-intervals
                        List valid intervals
    -f <fmt>            Date format
    -r <reten>          Retention specification
    -i <interval_seconds>
                        Jump this many seconds forward in time at each iteration
                        of the simulation
    -c, --create        Create snapshots at the interval specified by -i
    -l, --keep-latest   Keep latest
    -y, --keep-younger  Keep younger
    -p, --prompt        Waits for <Enter> between runs

"""
import sys
from datetime import datetime, timedelta
import snapshot_date_filter as sdf
from docopt import docopt

def simulate(
    snapdates, reten, interval, keep_latest=False, keep_younger=False,
    create=False, prompt=False, now=None
):
    snapdates = list(snapdates)
    if not now:
        try:
            now = max(snapdates)
        except ValueError:
            sdf.error_exit("Empty snapshot list")


    i = 0
    while True:
        print(f"RUN {i}  NOW {now.strftime('%Y-%m-%d_%H.%M.%S')}")
        if not snapdates:
            sdf.ok_exit("No more snapshots")
        output_dates = sdf.date_filter(
            keep=True, snapdates=snapdates, reten=reten, now=now,
            keep_latest=keep_latest, keep_younger=keep_younger
        )
        for output_date in output_dates:
            print(output_date.strftime(fmt))
        if prompt:
            input()
        print()
        now += timedelta(seconds=interval)
        if create:
            output_dates.append(now)
        snapdates = output_dates
        i += 1


if __name__ == "__main__":
    error_exit = sdf.error_exit
    ok_exit = sdf.ok_exit
    args = docopt(__doc__, version='simulate.py 0.1')
    if args["--list-valid-intervals"]:
        ok_exit(sdf.list_valid_intervals())
    fmt = args["-f"]
    try:
        reten = sdf.parse_reten_spec(args["-r"])
    except ValueError as e:
        error_exit(e)
    keep_latest = args["--keep-latest"]
    keep_younger = args["--keep-younger"]
    try:
        interval = int(args["-i"])
    except ValueError:
        error_exit("-i requires a numeric value")
    create = args["--create"]
    prompt = args["--prompt"]
    input_snapnames = sys.stdin.read().split("\n")

    input_snapdates = sdf.parse_dates(input_snapnames, fmt)

    simulate(
        input_snapdates, reten, interval, keep_latest=keep_latest,
        keep_younger=keep_younger, create=create, prompt=prompt
    )
