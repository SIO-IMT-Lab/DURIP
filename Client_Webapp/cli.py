"""Command line interface for managing sensor schedules."""

import argparse
from typing import List

from services.schedule_manager import ScheduleManager


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sensor Control System")
    subparsers = parser.add_subparsers(dest="command")

    parser_add = subparsers.add_parser("add", help="Add a new schedule")
    parser_add.add_argument("sensor", help="Sensor to schedule")
    parser_add.add_argument("start", help="Start time (HH:MM)")
    parser_add.add_argument("end", help="End time (HH:MM)")
    parser_add.add_argument("state", choices=["on", "off", "logging"], help="State during the schedule")
    parser_add.add_argument("--repeat", action="store_true", help="Repeat the schedule")
    parser_add.add_argument("--days", help="Comma separated days e.g. Mon,Tue")
    parser_add.add_argument("--end-repeat", dest="end_repeat", help="End repeat date (YYYY-MM-DD)")

    parser_remove = subparsers.add_parser("remove", help="Remove a schedule")
    parser_remove.add_argument("sensor", help="Sensor to remove schedule from")
    parser_remove.add_argument("index", type=int, help="Schedule index")

    subparsers.add_parser("view", help="View all schedules")
    subparsers.add_parser("view_states", help="View current states")

    parser_override = subparsers.add_parser("override", help="Override a sensor state")
    parser_override.add_argument("sensor", help="Sensor name or comma separated list")
    parser_override.add_argument("state", choices=["on", "off", "logging"], help="State to set")

    parser_remove_override = subparsers.add_parser("remove_override", help="Remove sensor override")
    parser_remove_override.add_argument("sensor", help="Sensor name or comma separated list")

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    manager = ScheduleManager()
    if args.command == "add":
        days = ScheduleManager._parse_days(args.days) if args.days else None
        print(
            manager.add_schedule(
                args.sensor,
                args.start,
                args.end,
                args.state,
                args.repeat,
                days,
                args.end_repeat,
            )
        )
    elif args.command == "remove":
        print(manager.remove_schedule(args.sensor, args.index))
    elif args.command == "view":
        print(manager.view_schedules())
    elif args.command == "view_states":
        print(manager.view_states())
    elif args.command == "override":
        sensors: List[str] = args.sensor.split(",")
        print(manager.override_sensor(sensors, args.state))
    elif args.command == "remove_override":
        sensors = args.sensor.split(",")
        print(manager.remove_override(sensors))
    else:
        raise SystemExit("No command provided")


if __name__ == "__main__":
    main()
