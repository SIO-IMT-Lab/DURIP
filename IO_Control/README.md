# IO Control Scripts

This folder provides command line utilities and GUIs for interacting with the
ADS1015 analog-to-digital converters and the MCP23017 GPIO expander over I2C.

## Scripts

- `gui.py` – combined GUI showing live ADS1015 voltages and allowing control of
  MCP23017 pins.
- `ads/ads.py` – command line utility printing scaled ADS1015 voltages.
- `ads/ads_gui.py` – GUI showing live voltages from one or more ADS1015 chips.
- `mcp/mcp.py` – interactive shell for toggling MCP23017 A pins.
- `mcp/mcp_gui.py` – GUI for toggling MCP23017 A and B pins.

Each script exposes configuration options such as I2C addresses and update
intervals through a command line interface using `argparse`.

## Installation

These utilities rely on the Adafruit CircuitPython libraries. Install the
required packages with:

```bash
pip install adafruit-circuitpython-ads1x15 adafruit-circuitpython-mcp230xx matplotlib
```

## Example

Run the combined GUI with custom ADS1015 addresses and a two-second refresh
interval:

```bash
python gui.py --ads-addresses 0x48 0x49 --mcp-address 0x20 --interval 2
```

Refer to the README files in `ads/` and `mcp/` for module-specific examples.
