import time
"""Combined ADS1015 and MCP23017 GUI with configurable options."""

import argparse
import threading
import time
import board
import busio
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from adafruit_ads1x15.ads1015 import ADS1015
from adafruit_ads1x15.analog_in import AnalogIn
from adafruit_mcp230xx.mcp23017 import MCP23017
import digitalio


def run_gui(ads_addresses: list[int], mcp_address: int, ratio: float, interval: float) -> None:
    """Launch the combined ADS1015/MCP23017 GUI."""

    i2c = busio.I2C(board.SCL, board.SDA)
    ads_devices = [ADS1015(i2c, address=a) for a in ads_addresses]
    ads_channels = [[AnalogIn(dev, ch) for ch in range(4)] for dev in ads_devices]
    data = [0.0] * (4 * len(ads_devices))

    mcp = MCP23017(i2c, address=mcp_address)
    a_pins: list[digitalio.DigitalInOut] = []
    b_pins: list[digitalio.DigitalInOut] = []
    for pin_num in range(8):
        a = mcp.get_pin(pin_num)
        b = mcp.get_pin(pin_num + 8)
        a.direction = digitalio.Direction.OUTPUT
        b.direction = digitalio.Direction.OUTPUT
        a.value = False
        b.value = False
        a_pins.append(a)
        b_pins.append(b)

    def update_data() -> None:
        while True:
            for dev_idx, ch_list in enumerate(ads_channels):
                for ch_idx, ch in enumerate(ch_list):
                    data[dev_idx * 4 + ch_idx] = ch.voltage * ratio
            time.sleep(interval)

    threading.Thread(target=update_data, daemon=True).start()

    root = tk.Tk()
    root.title("ADS1015 + MCP23017 GUI")

    main_frame = ttk.Frame(root, padding=10)
    main_frame.grid(row=0, column=0)

    ads_frame = ttk.Frame(main_frame, padding=10)
    ads_frame.grid(row=0, column=0)

    mcp_frame = ttk.Frame(main_frame, padding=10)
    mcp_frame.grid(row=0, column=1)

    ads_labels: list[ttk.Label] = []
    for i in range(len(data)):
        label = ttk.Label(ads_frame, text=f"Channel {i}: --- V", font=("Arial", 12))
        label.grid(row=i, column=0, sticky=tk.W)
        ads_labels.append(label)

    fig = Figure(figsize=(5, 3), dpi=100)
    ax = fig.add_subplot(111)
    bars = ax.bar(range(len(data)), data)
    ax.set_ylim(0, 30)
    ax.set_ylabel("Voltage (V)")
    ax.set_title("ADS1015 Voltages")
    ax.set_xticks(range(len(data)))
    ax.set_xticklabels([f"Ch {i}" for i in range(len(data))])
    canvas = FigureCanvasTkAgg(fig, master=ads_frame)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=1, rowspan=len(data))

    a_indicators: list[tk.Label] = []
    b_indicators: list[tk.Label] = []

    def update_indicators() -> None:
        for i, pin in enumerate(a_pins):
            a_indicators[i].config(bg="green" if pin.value else "red")
        for i, pin in enumerate(b_pins):
            b_indicators[i].config(bg="green" if pin.value else "red")

    def toggle_pin(pins: list[digitalio.DigitalInOut], idx: int) -> None:
        pins[idx].value = not pins[idx].value
        update_indicators()

    def set_pin(pins: list[digitalio.DigitalInOut], idx: int, state: bool) -> None:
        pins[idx].value = state
        update_indicators()

    def create_pin_controls(
        frame: ttk.Frame,
        label_prefix: str,
        pins: list[digitalio.DigitalInOut],
        indicators: list[tk.Label],
    ) -> None:
        section = ttk.LabelFrame(frame, text=f"{label_prefix} Pins", padding=5)
        section.pack(padx=5, pady=5)
        for i in range(8):
            row = ttk.Frame(section)
            row.pack(anchor="w")
            ttk.Label(row, text=f"{label_prefix}{i}", width=4).pack(side="left")
            ind = tk.Label(row, text=" ", bg="red", width=2, height=1, relief="groove")
            ind.pack(side="left", padx=5)
            indicators.append(ind)
            ttk.Button(row, text="Toggle", command=lambda i=i: toggle_pin(pins, i)).pack(side="left")
            ttk.Button(row, text="ON", command=lambda i=i: set_pin(pins, i, True)).pack(side="left")
            ttk.Button(row, text="OFF", command=lambda i=i: set_pin(pins, i, False)).pack(side="left")

    create_pin_controls(mcp_frame, "A", a_pins, a_indicators)
    create_pin_controls(mcp_frame, "B", b_pins, b_indicators)

    def refresh_gui() -> None:
        for i, label in enumerate(ads_labels):
            label.config(text=f"Channel {i}: {data[i]:.2f} V")
            bars[i].set_height(data[i])
        canvas.draw()
        update_indicators()
        root.after(int(interval * 1000), refresh_gui)

    root.after(int(interval * 1000), refresh_gui)
    root.mainloop()


def main() -> None:
    parser = argparse.ArgumentParser(description="Combined ADS1015/MCP23017 GUI")
    parser.add_argument(
        "--ads-addresses",
        nargs="+",
        default=["0x48", "0x49"],
        help="I2C addresses of ADS1015 chips (default: 0x48 0x49)",
    )
    parser.add_argument(
        "--mcp-address",
        type=lambda x: int(x, 0),
        default="0x20",
        help="I2C address of MCP23017 (default: 0x20)",
    )
    parser.add_argument(
        "--ratio",
        type=float,
        default=24 / 2.17,
        help="Scaling ratio volts/volts (default: 24/2.17)",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=1.0,
        help="Refresh interval in seconds (default: 1.0)",
    )
    args = parser.parse_args()
    ads_addresses = [int(a, 0) for a in args.ads_addresses]
    run_gui(ads_addresses, args.mcp_address, args.ratio, args.interval)


if __name__ == "__main__":
    main()
