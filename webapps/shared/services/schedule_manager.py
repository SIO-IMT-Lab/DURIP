from __future__ import annotations

import datetime
import json
from pathlib import Path
from typing import Dict, List, Optional

from crontab import CronTab


class ScheduleManager:
    """Manage sensor schedules, overrides and state persistence."""

    def __init__(self, storage_file: Optional[str] = None) -> None:
        shared_dir = Path(__file__).resolve().parent.parent
        self.scripts_dir = shared_dir / "scripts"
        default_storage = shared_dir / "schedule_files" / "sensor_schedule.json"
        self.storage_file = Path(storage_file) if storage_file else default_storage
        self.sensors_channels: Dict[str, int] = {
            "cDAQ": 1,
            "AML": 2,
            "subNero": 5,
            "FSO": 6,
            "TX": 7,
            "UV": 8,
        }
        self.sensors_state: Dict[str, str] = {key: "off" for key in self.sensors_channels}
        self.sensors_schedule, self.sensors_override, self.sensors_indices = self._load_from_storage()

    # ------------------------------------------------------------------
    # Persistence helpers
    def _load_from_storage(self) -> tuple[Dict[str, list], Dict[str, Optional[str]], Dict[str, int]]:
        """Load schedules, overrides and indices from the storage file."""
        try:
            with open(self.storage_file, "r") as file:
                data = json.load(file)
            schedules = data.get("schedules", {key: [] for key in self.sensors_channels})
            overrides = data.get("overrides", {key: None for key in self.sensors_channels})
            indices = data.get("indices", {key: 0 for key in self.sensors_channels})
        except FileNotFoundError:
            schedules = {key: [] for key in self.sensors_channels}
            overrides = {key: None for key in self.sensors_channels}
            indices = {key: 0 for key in self.sensors_channels}
            self._save_to_storage(schedules, overrides, indices)
        return schedules, overrides, indices

    def _save_to_storage(
        self,
        schedules: Dict[str, list],
        overrides: Dict[str, Optional[str]],
        indices: Dict[str, int],
    ) -> None:
        data = {"schedules": schedules, "overrides": overrides, "indices": indices}
        with open(self.storage_file, "w") as file:
            json.dump(data, file, indent=4)

    def _persist(self) -> None:
        """Persist current schedules and overrides to storage."""
        self._save_to_storage(self.sensors_schedule, self.sensors_override, self.sensors_indices)

    # ------------------------------------------------------------------
    # Utility parsing helpers
    @staticmethod
    def _parse_date(date_str: str) -> datetime.date:
        return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()

    @staticmethod
    def _parse_days(days_str: str) -> List[int]:
        days_map = {"Mon": 1, "Tue": 2, "Wed": 3, "Thu": 4, "Fri": 5, "Sat": 6, "Sun": 0}
        return [days_map[day] for day in days_str.split(",") if day in days_map]

    # ------------------------------------------------------------------
    # Cron helpers
    def _add_crontab_job(self, sensor: str, state: str, time: str, tag: str) -> None:
        cron = CronTab(user=True)
        if state == "logging":
            command = (
                f'echo "Sensor {sensor} is now logging" '
                f'&& python {self.scripts_dir / "LogSerialData.py"}'
            )
        else:
            channel = self.sensors_channels[sensor]
            command = (
                f'echo "Sensor {sensor} is now in state {state}" '
                f'&& /home/admin/8mosfet-rpi/8mosfet 0 write {channel} {state}'
            )
        job = cron.new(command=command, comment=tag)
        job.setall(time)
        cron.write()

    # ------------------------------------------------------------------
    # Schedule operations
    def add_schedule(
        self,
        sensor: str,
        start: str,
        end: str,
        state: str,
        repeat: bool = False,
        days: Optional[List[int]] = None,
        end_repeat: Optional[str] = None,
    ) -> str:
        """Add a schedule for ``sensor`` and create corresponding cron jobs."""
        schedule_index = self.sensors_indices[sensor]
        schedule = {
            "start": start,
            "end": end,
            "repeat": repeat,
            "state": state,
            "days": days,
            "end_repeat": end_repeat,
            "id": schedule_index,
        }
        self.sensors_indices[sensor] += 1
        self.sensors_schedule[sensor].append(schedule)

        start_hours, start_minutes = start.split(":")
        end_hours, end_minutes = end.split(":")
        start_tag = f"sensor_{sensor}_schedule_{schedule_index}_start"
        end_tag = f"sensor_{sensor}_schedule_{schedule_index}_end"

        cron_dates = "*"
        cron_days = "*"
        cron_months = "*"
        if not repeat:
            if days:
                next_occurrence = datetime.datetime.now().date()
                while next_occurrence.weekday() not in days:
                    next_occurrence += datetime.timedelta(days=1)
                cron_dates = next_occurrence.strftime("%d")
                cron_months = next_occurrence.strftime("%m")
            else:
                today = datetime.datetime.now().date()
                cron_dates = today.strftime("%d")
                cron_months = today.strftime("%m")
                cron_days = str(today.isoweekday())
            start_time_cron = f"{start_minutes} {start_hours} {cron_dates} {cron_months} {cron_days}"
            end_time_cron = f"{end_minutes} {end_hours} {cron_dates} {cron_months} {cron_days}"
            self._add_crontab_job(sensor, state, start_time_cron, start_tag)
            self._add_crontab_job(sensor, "off", end_time_cron, end_tag)
        else:
            if days:
                cron_days = ",".join(str(day) for day in days)
            if end_repeat:
                end_date = self._parse_date(end_repeat)
                cron_months = f"{datetime.datetime.now().month}-{end_date.month}"
                cron_dates = f"{datetime.datetime.now().isoweekday()}-{end_date.isoweekday()}"
            start_time_cron = f"{start_minutes} {start_hours} {cron_dates} {cron_months} {cron_days}"
            end_time_cron = f"{end_minutes} {end_hours} {cron_dates} {cron_months} {cron_days}"
            self._add_crontab_job(sensor, state, start_time_cron, start_tag)
            self._add_crontab_job(sensor, "off", end_time_cron, end_tag)

        self._persist()
        return f"Schedule added for {sensor} with state '{state}' [Index: #{schedule_index}]."

    def remove_schedule(self, sensor: str, index: int) -> str:
        for i, schedule in enumerate(self.sensors_schedule[sensor]):
            if schedule["id"] == index:
                self.sensors_schedule[sensor].pop(i)
                break
        else:
            raise ValueError("Invalid schedule index.")

        cron = CronTab(user=True)
        tag_start = f"sensor_{sensor}_schedule_{index}_start"
        tag_end = f"sensor_{sensor}_schedule_{index}_end"
        for job in cron:
            if job.comment in {tag_start, tag_end}:
                cron.remove(job)
        cron.write()
        self._persist()
        return f"Schedule {index} removed from sensor {sensor}."

    def view_schedules(self) -> str:
        lines: List[str] = []
        for sensor, schedules in self.sensors_schedule.items():
            override = self.sensors_override[sensor]
            override_text = f" (OVERRIDE: {override})" if override else ""
            lines.append(f"{sensor}{override_text} Schedules:")
            for schedule in schedules:
                lines.append(
                    f"{schedule['id']}: Start: {schedule['start']}, End: {schedule['end']}, Repeat: {schedule['repeat']}"
                )
            lines.append("")
        return "\n".join(lines)

    def view_states(self) -> str:
        lines: List[str] = []
        now = datetime.datetime.now().time()
        for sensor, _ in self.sensors_state.items():
            override = self.sensors_override[sensor]
            if override:
                lines.append(f"{sensor}: {override} (OVERRIDE)")
                continue
            found = False
            for schedule in self.sensors_schedule[sensor]:
                start_time = datetime.datetime.strptime(schedule["start"], "%H:%M").time()
                end_time = datetime.datetime.strptime(schedule["end"], "%H:%M").time()
                if start_time <= now <= end_time:
                    lines.append(f"{sensor}: {schedule['state']} (SCHEDULED)")
                    found = True
                    break
            if not found:
                lines.append(f"{sensor}: off")
        return "\n".join(lines)

    def override_sensor(self, sensors: List[str], state: str) -> str:
        cron = CronTab(user=True)
        for sensor in sensors:
            self.sensors_state[sensor] = state
            self.sensors_override[sensor] = state
            for job in cron.find_comment(f"sensor_{sensor}_schedule_"):
                job.enable(False)
            if state == "logging":
                command = (
                    f'echo "Sensor {sensor} is now logging" '
                    f'&& python {self.scripts_dir / "LogSerialData.py"}'
                )
            else:
                channel = self.sensors_channels[sensor]
                command = (
                    f'echo "Sensor {sensor} is now overridden to state {state}" '
                    f'&& /home/admin/8mosfet-rpi/8mosfet 0 write {channel} {state}'
                )
            job = cron.new(command=command, comment=f"override_{sensor}")
            job.setall("* * * * *")
        cron.write()
        self._persist()
        return f"Sensors {', '.join(sensors)} overridden to '{state}'."

    def remove_override(self, sensors: List[str]) -> str:
        cron = CronTab(user=True)
        for sensor in sensors:
            self.sensors_override[sensor] = None
            for job in cron.find_comment(f"override_{sensor}"):
                cron.remove(job)
            for job in cron.find_comment(f"sensor_{sensor}_schedule_"):
                job.enable(True)
        cron.write()
        self._persist()
        return f"Override removed for sensors {', '.join(sensors)}."

    # ------------------------------------------------------------------
    # Dispatcher used by API
    def execute(self, command: str, args: List[str]) -> str:
        if command == "add":
            if len(args) < 4:
                raise ValueError("Insufficient arguments for add")
            sensor, start, end, state, *rest = args
            repeat = rest[0].lower() == "true" if rest else False
            days = self._parse_days(rest[1]) if len(rest) > 1 and rest[1] else None
            end_repeat = rest[2] if len(rest) > 2 and rest[2] else None
            return self.add_schedule(sensor, start, end, state, repeat, days, end_repeat)
        if command == "remove":
            sensor, index = args
            return self.remove_schedule(sensor, int(index))
        if command == "override":
            sensor, state = args
            return self.override_sensor(sensor.split(","), state)
        if command == "remove_override":
            sensor = args[0]
            return self.remove_override(sensor.split(","))
        if command == "view":
            return self.view_schedules()
        if command == "view_states":
            return self.view_states()
        raise ValueError(f"Unknown command: {command}")
