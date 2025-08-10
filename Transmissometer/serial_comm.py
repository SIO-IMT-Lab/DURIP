"""Log transmissometer data from a serial port.

This script reads lines from a serial device and appends them to a log file
with a timestamp. Serial parameters and the log file location can be
configured through command-line arguments.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import time

import serial


DEFAULT_PORT = "/dev/tty.usbserial-FT9EJUFK1"
DEFAULT_BAUDRATE = 19200
DEFAULT_LOG = "TX.txt"


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(
        description="Log transmissometer readings from a serial connection."
    )
    parser.add_argument(
        "-p",
        "--port",
        default=DEFAULT_PORT,
        help=f"Serial device path (default: {DEFAULT_PORT})",
    )
    parser.add_argument(
        "-b",
        "--baudrate",
        type=int,
        default=DEFAULT_BAUDRATE,
        help=f"Baud rate for the serial connection (default: {DEFAULT_BAUDRATE})",
    )
    parser.add_argument(
        "-l",
        "--log-file",
        type=Path,
        default=DEFAULT_LOG,
        help=f"File to append logged data to (default: {DEFAULT_LOG})",
    )
    return parser.parse_args()


def main() -> None:
    """Run the serial logger."""

    args = parse_args()
    timestamp_fmt = "%Y-%m-%d %H:%M:%S"

    print(
        f"Opening serial port {args.port} at {args.baudrate} baud. "
        f"Logging to {args.log_file}"
    )

    try:
        with serial.Serial(args.port, args.baudrate, timeout=1) as ser, open(
            args.log_file, "a", encoding="utf-8"
        ) as log_file:
            while True:
                if ser.in_waiting:
                    data = ser.readline()
                    timestamp = time.strftime(timestamp_fmt)
                    text = data.decode("utf-8", errors="replace")
                    line = f"{timestamp} - {text}"
                    log_file.write(line)
                    print(line, end="")
    except serial.SerialException as exc:
        print(f"Serial error: {exc}")
    except KeyboardInterrupt:
        print("\nExiting.")


if __name__ == "__main__":
    main()

