import argparse
import datetime
from crontab import CronTab
import json

storage_file = 'sensor_schedule.json'
sensors_schedule = {"cDAQ": [], "AML": [], "subNero": [], "FSO": [], "TX": [], "UV": []}
sensors_state = {"cDAQ": "off", "AML": "off", "subNero": "off", "FSO": "off", "TX": "off", "UV": "off"}  # State can now be 'off', 'on', or 'logging'
sensors_override = {"cDAQ": None, "AML": None, "subNero": None, "FSO": None, "TX": None, "UV": None}  # Override can be 'off', 'on', or 'logging'
sensors_indices = {"cDAQ": 0, "AML": 0, "subNero": 0, "FSO": 0, "TX": 0, "UV": 0}
sensors_channels = {"cDAQ": 1, "AML": 2, "subNero": 5, "FSO": 6, "TX": 7, "UV": 8} # 8mosfet channel for each sensor

def load_from_storage():
    """Load the schedules and overrides from the JSON storage."""
    try:
        with open(storage_file, 'r') as file:
            data = json.load(file)
        return data['schedules'], data['overrides'], data['indices']
    except FileNotFoundError:
        print("No storage file found. Do you want to create a new one? (y/n)")
        response = input()
        if response.lower() == 'y':
            return {"cDAQ": [], "AML": [], "subNero": [], "FSO": [], "TX": [], "UV": []}, {"cDAQ": None, "AML": None, "subNero": None, "FSO": None, "TX": None, "UV": None}, {"cDAQ": 0, "AML": 0, "subNero": 0, "FSO": 0, "TX": 0, "UV": 0}
        else:
            print(f"Exiting. Please make sure that the storage file is called '{storage_file}'.")
            exit()

# Load the schedules and overrides from the JSON storage
sensors_schedule, sensors_override, sensors_indices = load_from_storage()

def save_to_storage(schedules, overrides, indices):
    """Save the schedules and overrides to the JSON storage."""
    data = {
        'schedules': schedules,
        'overrides': overrides,
        'indices': indices
    }
    with open(storage_file, 'w') as file:
        json.dump(data, file, indent=4)

def add_crontab_job(sensor, state, time, tag):
    """Add a crontab job to change the sensor state at a specified time, with a unique tag."""
    cron = CronTab(user=True)
    if state == 'logging':
        command = f'echo \"Sensor {sensor} is now logging\" && python LogSerialData.py'
    else:
        command = f'echo \"Sensor {sensor} is now in state {state}\" && /home/admin/8mosfet-rpi/8mosfet 0 write {sensors_channels[sensor]} {state}'
    job = cron.new(command=command, comment=tag)
    job.setall(time)
    cron.write()
    print(f"Crontab job added for sensor {sensor} to turn {state} at {time} with tag '{tag}'.")

def parse_date(date_str):
    """Parse a date string in the format YYYY-MM-DD."""
    return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()

def parse_days(days_str):
    """Parse a comma-separated string of days."""
    days_map = {"Mon": 1, "Tue": 2, "Wed": 3, "Thu": 4, "Fri": 5, "Sat": 6, "Sun": 0}
    return [days_map[day] for day in days_str.split(',') if day in days_map]

def add_schedule(args):
    """Adds a schedule for a sensor or multiple sensors and creates crontab jobs with unique tags."""
    sensors = args.sensor.split(',')
    start_time = args.start  # Assuming this is in HH:MM format
    end_time = args.end  # Assuming this is in HH:MM format
    repeat = args.repeat
    state = args.state  # The desired state ('on', 'off', 'logging')
    days = parse_days(args.days) if args.days else None
    end_repeat = parse_date(args.end_repeat) if args.end_repeat else None

    for sensor in sensors:
        # Add the schedule to the sensor's schedule list
        schedule_index = sensors_indices[sensor]
        
        schedule = {
            "start": start_time, 
            "end": end_time, 
            "repeat": repeat, 
            "state": state, 
            "days": days,
            "end_repeat": args.end_repeat,
            "id": schedule_index
        }
        sensors_indices[sensor] += 1
        sensors_schedule[sensor].append(schedule)
        print(f"Schedule added for sensor {sensor} with state '{state}' [Index: #{schedule_index}].")

        # Convert start and end times to cron format
        start_hours, start_minutes = start_time.split(':')
        end_hours, end_minutes = end_time.split(':')

        # Define the tag for crontab jobs
        start_tag = f"sensor_{sensor}_schedule_{schedule_index}_start"
        end_tag = f"sensor_{sensor}_schedule_{schedule_index}_end"

        # Handle different repeat patterns
        cron_dates = '*'
        cron_days = '*'
        cron_months = '*'

        if not repeat:
            # For a single occurrence, check if days parameter is specified
            if days:
                next_occurrence = datetime.datetime.now().date()
                while next_occurrence.weekday() not in days:
                    next_occurrence += datetime.timedelta(days=1)
                cron_dates = next_occurrence.strftime('%d')
                cron_months = next_occurrence.strftime('%m')
            else:
                end_repeat = datetime.datetime.now().date()
                cron_dates = end_repeat.strftime('%d')
                cron_months = end_repeat.strftime('%m')
                cron_days = end_repeat.isoweekday()

            start_time_cron = f"{start_minutes} {start_hours} {cron_dates} {cron_months} {cron_days}"
            end_time_cron = f"{end_minutes} {end_hours} {cron_dates} {cron_months} {cron_days}"
            add_crontab_job(sensor, state, start_time_cron, start_tag)
            add_crontab_job(sensor, 'off', end_time_cron, end_tag)
        else:
            # Weekly or custom with specified days
            if days:
                cron_days = ','.join(str(day) for day in days)
            if end_repeat:
                cron_months = f"{datetime.datetime.now().month}-{end_repeat.month}"
                cron_dates = f"{datetime.datetime.now().isoweekday()}-{end_repeat.isoweekday()}"

            # Create start and end crontab jobs for each schedule
            start_time_cron = f"{start_minutes} {start_hours} {cron_dates} {cron_months} {cron_days}"
            end_time_cron = f"{end_minutes} {end_hours} {cron_dates} {cron_months} {cron_days}"
            add_crontab_job(sensor, state, start_time_cron, start_tag)
            add_crontab_job(sensor, 'off', end_time_cron, end_tag)

        # Save updates to storage after adding all schedules
        save_to_storage(sensors_schedule, sensors_override, sensors_indices)

def remove_schedule(args):
    """Removes a schedule from a sensor and deletes corresponding crontab jobs."""
    sensor = args.sensor
    schedule_index = args.index
    if schedule_index < sensors_indices[sensor] + 1:
        # Remove the schedule
        for i, schedule in enumerate(sensors_schedule[sensor]):
            print(schedule)
            if schedule['id'] == schedule_index:
                sensors_schedule[sensor].pop(i)

        print(f"Schedule {schedule_index} removed from sensor {sensor}.")

        # Remove corresponding crontab jobs
        cron = CronTab(user=True)
        tag_start = f"sensor_{sensor}_schedule_{schedule_index}_start"
        tag_end = f"sensor_{sensor}_schedule_{schedule_index}_end"
        jobs_to_remove = [job for job in cron if job.comment == tag_start or job.comment == tag_end]
        for job in jobs_to_remove:
            cron.remove(job)
        cron.write()
        print(f"Crontab jobs with tag '{tag_start}' and '{tag_end}' removed.")

        # Save updates to storage
        save_to_storage(sensors_schedule, sensors_override, sensors_indices)
    else:
        print("Invalid schedule index.")


def view_schedules(args):
    """Displays the schedules of all sensors."""
    for sensor, schedules in sensors_schedule.items():
        if sensors_override[sensor] is not None:
            override = f" (OVERRIDE: {sensors_override[sensor]})"
        else:
            override = ""
        print(f"{sensor}{override} Schedules:")
        for i, schedule in enumerate(schedules):
            print(f"{schedule['id']}: Start: {schedule['start']}, End: {schedule['end']}, Repeat: {schedule['repeat']}")
        print("")

def view_states(args):
    """Displays the states and overrides of all sensors."""
    # Note: this should be done based on the current time, and whatever is in the crontab

    for sensor, state in sensors_state.items():
        if sensors_override[sensor] is not None:
            print(f"{sensor}: {sensors_override[sensor]} (OVERRIDE)")
        else:
            current_time = datetime.datetime.now().time()   
            found = False
            for schedule in sensors_schedule[sensor]:
                start_time = datetime.datetime.strptime(schedule['start'], "%H:%M").time()
                end_time = datetime.datetime.strptime(schedule['end'], "%H:%M").time()
                if start_time <= current_time <= end_time:
                    print(f"{sensor}: {schedule['state']} (SCHEDULED)")
                    found = True
                    break

            if not found:
                print(f"{sensor}: off")

def override_sensor(args):
    """Overrides the state of one or more sensors and manages crontab jobs accordingly."""
    sensors = args.sensor.split(',')
    state = args.state.lower()  # State can now also be 'logging'

    cron = CronTab(user=True)
    for sensor in sensors:
        sensors_state[sensor] = state
        sensors_override[sensor] = state

        # Disable all existing jobs for this sensor
        for job in cron.find_comment(f"sensor_{sensor}_schedule_"):
            job.enable(False)

        # Add a temporary override job
        if state == 'logging':
            command = f'echo \"Sensor {sensor} is now logging\" && python LogSerialData.py'
        else:
            command = f'echo \"Sensor {sensor} is now overridden to state {state}\" && /home/admin/8mosfet-rpi/8mosfet 0 write {sensors_channels[sensor]} {state}'

        # Assuming override is immediate, no specific time provided, runs every minute
        job = cron.new(command=command, comment=f"override_{sensor}")
        job.setall("* * * * *")  # Every minute; adjust if you need less frequency
        cron.write()

        print(f"Sensor {sensor} overridden to '{state}'. Existing schedules disabled, override job added.")

def remove_override(args):
    """Removes the override from one or more sensors and restores original crontab jobs."""
    sensors = args.sensor.split(',')

    cron = CronTab(user=True)
    for sensor in sensors:
        # Clear override state
        sensors_override[sensor] = None

        # Remove the temporary override job
        for job in cron.find_comment(f"override_{sensor}"):
            cron.remove(job)

        # Re-enable all original jobs for this sensor
        for job in cron.find_comment(f"sensor_{sensor}_schedule_"):
            job.enable(True)
        
        cron.write()

        print(f"Override removed for sensor {sensor}. Override job deleted, original schedules restored.")

def main():
    parser = argparse.ArgumentParser(description="Sensor Control System")
    subparsers = parser.add_subparsers(dest='command')

     # Subparser for adding a schedule now includes a state argument
    parser_add = subparsers.add_parser('add', help='Add a new schedule')
    parser_add.add_argument('sensor', help='Sensor(s) to schedule (comma-separated for multiple sensors)')
    parser_add.add_argument('start', help='Start time (HH:MM)')
    parser_add.add_argument('end', help='End time (HH:MM)')
    parser_add.add_argument('state', choices=['on', 'off', 'logging'], help='State during the schedule')
    parser_add.add_argument('--repeat', action='store_true', help='Whether to repeat the schedule')
    parser_add.add_argument('--days', help='Days of the week to repeat (comma-separated, e.g. Mon,Tue,Wed)')
    parser_add.add_argument('--end-repeat', help='End repeat date (YYYY-MM-DD) for custom repeat')

    # Subparser for removing a schedule
    parser_remove = subparsers.add_parser('remove', help='Remove a schedule')
    parser_remove.add_argument('sensor', choices=sensors_schedule.keys(), help='Sensor to remove schedule from')
    parser_remove.add_argument('index', type=int, help='Index of schedule to remove')

    # Subparser for viewing schedules
    parser_view = subparsers.add_parser('view', help='View all schedules')
    parser_states = subparsers.add_parser('view_states', help='View all states')

    # Subparser for overriding a sensor now includes 'logging' in the choices
    parser_override = subparsers.add_parser('override', help='Override a sensor on, off, or to logging')
    parser_override.add_argument('sensor', help='Sensor(s) to override (comma-separated for multiple sensors)')
    parser_override.add_argument('state', choices=['on', 'off', 'logging'], help='State to set the sensor')

    # Subparser for removing an override
    parser_remove_override = subparsers.add_parser('remove_override', help='Remove override from a sensor')
    parser_remove_override.add_argument('sensor', help='Sensor(s) to remove override from (comma-separated for multiple sensors)')

    args = parser.parse_args()

    if args.command == 'add':
        add_schedule(args)
    elif args.command == 'remove':
        remove_schedule(args)
    elif args.command == 'view':
        view_schedules(args)
    elif args.command == 'override':
        override_sensor(args)
    elif args.command == 'remove_override':
        remove_override(args)
    elif args.command == 'view_states':
        view_states(args)
    else:
        parser.print_help()

    save_to_storage(sensors_schedule, sensors_override, sensors_indices)

if __name__ == "__main__":
    main()
