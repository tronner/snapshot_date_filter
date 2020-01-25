snapshot_date_filter

Reads a list of snapshots on stdin, writes the snapshots to keep or remove
according to the given date format and retention specification to stdout.
Snapshots not matching the date format are ignored. Removed snapshots are
printed in reverse sorted order. All times are in UTC.

Usage:
  snapshot_date_filter (keep | remove) -f <fmt> -r <reten>
                       [-l | --keep-latest] [-y | --keep-younger]
  snapshot_date_filter (-h | --help | --version | -R | --list-valid-reten)

Options:
  -h, --help          Show this message
  --version           Show version
  -R, --list-valid-intervals
                      List all valid retention intervals
  -f <fmt>            Date format string
  -r <reten>          Retention specification (see -R option and example below)
  -l, --keep-latest   Always keep latest snapshot
  -y, --keep-younger  Keep snapshots younger than the youngest snapshot
                      according to the retention specification

Example:
  This example lists all zfs snapshots for mypool/data1 (example snapshot:
  `mypool/data1@auto-2019-08-25_18.30`), determines which snapshots to
  remove by piping through this script, and destroys those snapshots:

  zfs list -r -t snapshot -H -o name mypool/data1 \
      | snapshot_date_filter remove -f "mypool/data1@auto-%Y-%m-%d_%H.%M" -r "day 7 week 4 month 12 year 3" \
      | while read snapshot; do
          zfs destroy -v $snapshot
        done
