# AML Serial Communication

This directory contains a Python script for communicating with an AML
instrument over a serial port and logging the device's output.

## Usage

```bash
python serial_comm.py --port /dev/ttyUSB0 --baud 38400 --log AML.txt --command MONITOR
```

### Options

- `--port` – serial device path (defaults to `/dev/tty.usbserial-FT4YCM0W`)
- `--baud` – baud rate for the connection (defaults to `38400`)
- `--log` – path to the log file (defaults to `AML.txt`)
- `--command` – initial command sent to the device (defaults to `MONITOR`)

Stop the script with `Ctrl+C`.  All received data is appended to the
specified log file with a timestamp.

