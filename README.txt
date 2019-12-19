snapshot_date_filter

Reads a date sorted list of snapshots on stdin, writes the snapshots to keep
or remove to stdout. Removed snapshots are printed in reverse sorted order.

Usage:
  snapshot_date_filter (keep | remove) -f <fmt> -r <reten>
  snapshot_date_filter (-h | --help | --version)

Options:
  -h --help     Show this message
  --version     Show version
  -f <fmt>      Date format string
  -r <reten>    Retention specification (see example below and source code
                for a list of valid intervals)

Example:
  This example lists all zfs snapshots for mypool/data1, determines which
  snapshots to remove by running this script, and destroying those snapshots:

  zfs list -r -t snapshot -H -o name mypool/data1 \
      | snapshot_date_filter remove -f "mypool/data1@auto-%Y-%m-%d_%H.%M" -r "day 7 week 4 month 12 year 3" \
      | xargs zfs destroy

