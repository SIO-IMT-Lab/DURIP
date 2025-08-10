# Transmissometer Serial Logger

This directory contains a small Python script for logging data from the
Seabird transmissometer over a serial connection.

## Requirements

- Python 3
- [pyserial](https://pyserial.readthedocs.io/)

Install the dependency with:

```bash
pip install pyserial
```

## Usage

```bash
python serial_comm.py --port /dev/ttyUSB0 --baudrate 19200 --log-file TX.txt
```

Arguments:

- `--port` serial device path (defaults to `/dev/tty.usbserial-FT9EJUFK1`).
- `--baudrate` serial port baud rate (default `19200`).
- `--log-file` path to append the logged output (default `TX.txt`).

Press `Ctrl+C` to stop logging. Output is appended to the specified log file
with timestamps.


