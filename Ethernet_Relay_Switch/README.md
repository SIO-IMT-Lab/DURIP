# Ethernet Relay Switch

Utilities for controlling a two channel Ethernet relay.  The relay can
be operated from the command line or through a small graphical
application.

## `relay.py`

Sends a sequence of ASCII commands to the relay over TCP:

```bash
python relay.py --ip 192.168.1.100 --port 6722 --commands 1R 2R 00 2R 1R 00
```

### Options

- `--ip` – relay IP address (defaults to `192.168.1.100`)
- `--port` – TCP port (defaults to `6722`)
- `--commands` – space separated list of commands to send
- `--delay` – pause in seconds between commands (defaults to `0.5`)

## `relay_gui.py`

Launches a Tkinter based GUI to operate the relay:

```bash
python relay_gui.py --ip 192.168.1.100 --port 6722
```

### Options

- `--ip` – relay IP address (defaults to `192.168.1.100`)
- `--port` – TCP port (defaults to `6722`)
- `--timeout` – network timeout in seconds (defaults to `2.0`)

