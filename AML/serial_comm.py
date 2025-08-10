"""AML serial communication logger.

This script connects to an AML device over a serial port, sends a
command and logs any data returned by the device.  All configuration is
provided via a command line interface so the script can be reused in a
variety of environments without editing the source.
"""

from __future__ import annotations

import argparse
import time
from typing import Iterable

import serial


def log_data(log_file: str, data: bytes) -> None:
    """Append *data* to *log_file* with a timestamp."""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a", encoding="utf-8") as fh:
        fh.write(f"{timestamp} - {data.decode('utf-8')}")


def read_serial(port: str, baud: int, log_file: str, command: str) -> None:
    """Open *port* at *baud* and log replies to *log_file*.

    A single *command* is sent immediately after opening the port.  The
    script then continuously reads from the serial connection until the
    user presses :kbd:`Ctrl+C`.
    """

    print(f"Opening serial port {port} at {baud} baud…")
    with serial.Serial(port, baud, timeout=1) as ser:
        print("Serial port opened successfully.")
        print(f"Sending {command!r} to the device…")
        ser.write(f"{command}\r".encode())
        print("Waiting for device to respond…")
        time.sleep(1)

        try:
            while True:
                if ser.in_waiting > 0:
                    data = ser.readline()
                    log_data(log_file, data)
                    print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {data.decode('utf-8')}", end="")
        except KeyboardInterrupt:
            print("Exiting…")


def parse_args(args: Iterable[str] | None = None) -> argparse.Namespace:
    """Return parsed command line arguments."""

    parser = argparse.ArgumentParser(description="Log data from an AML serial device")
    parser.add_argument(
        "--port",
        default="/dev/tty.usbserial-FT4YCM0W",
        help="Serial port device path",
    )
    parser.add_argument(
        "--baud",
        type=int,
        default=38400,
        help="Baud rate for the serial connection",
    )
    parser.add_argument(
        "--log",
        default="AML.txt",
        help="Path to the log file",
    )
    parser.add_argument(
        "--command",
        default="MONITOR",
        help="Command to send to the device on start-up",
    )
    return parser.parse_args(args)


def main(argv: Iterable[str] | None = None) -> None:
    args = parse_args(argv)
    try:
        read_serial(args.port, args.baud, args.log, args.command)
    except serial.SerialException as exc:
        print(f"Serial error: {exc}")


if __name__ == "__main__":  # pragma: no cover - manual invocation
    main()

