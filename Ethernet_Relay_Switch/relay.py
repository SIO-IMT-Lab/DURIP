"""Simple command-line interface for a two-channel Ethernet relay.

The original script used hard coded values for the IP address, port and
command sequence.  This rewrite exposes those parameters via a command
line interface so it can easily be scripted in different environments.
"""

from __future__ import annotations

import argparse
import socket
import time
from typing import Iterable, List


DEFAULT_COMMANDS = ["1R", "2R", "00", "2R", "1R", "00"]


def send_commands(ip: str, port: int, commands: Iterable[str], delay: float) -> None:
    """Send *commands* to the relay at *ip*:*port* with a pause between each."""

    with socket.create_connection((ip, port), timeout=2) as s:
        for cmd in commands:
            s.sendall(cmd.encode())
            reply = s.recv(16)
            print(f"{cmd} -> {reply.decode(errors='ignore')}")
            time.sleep(delay)


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Control an Ethernet relay")
    parser.add_argument("--ip", default="192.168.1.100", help="IP address of the relay")
    parser.add_argument("--port", type=int, default=6722, help="TCP port of the relay")
    parser.add_argument(
        "--commands",
        nargs="*",
        default=DEFAULT_COMMANDS,
        help="Space separated list of commands to send in order",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.5,
        help="Delay in seconds between commands",
    )
    return parser.parse_args(argv)


def main(argv: Iterable[str] | None = None) -> None:
    args = parse_args(argv)
    send_commands(args.ip, args.port, args.commands, args.delay)


if __name__ == "__main__":  # pragma: no cover - manual invocation
    main()

