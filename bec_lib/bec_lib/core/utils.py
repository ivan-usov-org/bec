from __future__ import annotations

import functools
from typing import TYPE_CHECKING
from collections import defaultdict
import csv

if TYPE_CHECKING:
    from bec_lib.scan_manager import ScanReport


def threadlocked(fcn):
    """Ensure that the thread acquires and releases the lock."""

    @functools.wraps(fcn)
    def wrapper(self, *args, **kwargs):
        # pylint: disable=protected-access
        with self._lock:
            return fcn(self, *args, **kwargs)

    return wrapper


def to_csv(
    scan_report: ScanReport,
    output_name: str,
    delimiter: str = ",",
    header: list = None,
    write_metadata: bool = True,
) -> None:
    """Convert scan data to a csv file.

    Args:
        scan_report (ScanReport): Scan report object.
        filename (str): Name of the csv file.
        delimiter (str, optional): Delimiter for the csv file. Defaults to ",".
        header (list, optional): Header for the csv file. Defaults to None.
        write_metadata (bool, optional): If True, the metadata of the scan will be written to the header of csv file. Defaults to True.

        Examples:
            >>> to_csv(scan_report, "./scan.csv")"""
    scan_dict = scan_to_dict(scan_report, flat=True)
    header = list(scan_dict["value"].keys()) if header is None else header
    header[0] = "".join(["#", header[0]])
    with open(output_name, "w") as file:
        writer = csv.writer(file, delimiter=delimiter)
        if write_metadata:
            scan_metadata = str(scan_report)
            scan_metadata = ["#" + entry.replace("\t", "") for entry in scan_metadata.split("\n")]
            for line in scan_metadata:
                writer.writerow([line])
            scan_metadata = str(scan_report.scan)
            scan_metadata = ["#" + entry.replace("\t", "") for entry in scan_metadata.split("\n")]
            for line in scan_metadata:
                writer.writerow([line])
        writer.writerow(["#value"])
        writer.writerow(header)
        writer.writerows(zip(*scan_dict["value"].values()))
        writer.writerow(["#timestamp"])
        writer.writerow(header)
        writer.writerows(zip(*scan_dict["timestamp"].values()))


def scan_to_dict(scan_report: ScanReport, flat: bool = True) -> dict:
    """Convert scan data to a dictionary.

    Args:
        scan_report (ScanReport): Scan report object.
        flat (bool, optional): If True, the dictionary will be flat. Defaults to True.

    Returns:
        (dict): Dictionary of scan data.

    Examples:
        >>> scan_to_dict(scan_report) with scan_report = scans.line_scan(...)
    """
    if flat:
        scan_dict = {"timestamp": defaultdict(list), "value": defaultdict(list)}
    else:
        scan_dict = {
            "timestamp": defaultdict(lambda: defaultdict(list)),
            "value": defaultdict(lambda: defaultdict(list)),
        }

    for scan_msg in scan_report.scan.data.values():
        scan_msg_data = scan_msg.content["data"]
        for dev, dev_data in scan_msg_data.items():
            for signal, signal_data in dev_data.items():
                if flat:
                    scan_dict["timestamp"][signal].append(signal_data["timestamp"])
                    scan_dict["value"][signal].append(signal_data["value"])
                else:
                    scan_dict["timestamp"][dev][signal].append(signal_data["timestamp"])
                    scan_dict["value"][dev][signal].append(signal_data["value"])

    return scan_dict
