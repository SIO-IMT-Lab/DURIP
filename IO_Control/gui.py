import time
import threading
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

# === Constants ===
RATIO = 24 / 2.17  # volts / volts

# === Initialize I2C and Devices ===
i2c = busio.I2C(board.SCL, board.SDA)

ads1 = ADS1015(i2c, address=0x48)
ads2 = ADS1015(i2c, address=0x49)
ads1_channels = [AnalogIn(ads1, ch) for ch in [0, 1, 2, 3]]
ads2_channels = [AnalogIn(ads2, ch) for ch in [0, 1, 2, 3]]
data = [0] * 8

mcp = MCP23017(i2c, address=0x20)
a_pins = []
b_pins = []
for pin_num in range(8):
    a = mcp.get_pin(pin_num)
    b = mcp.get_pin(pin_num + 8)
    a.direction = digitalio.Direction.OUTPUT
    b.direction = digitalio.Direction.OUTPUT
    a.value = False
    b.value = False
    a_pins.append(a)
    b_pins.append(b)

# === Data Update Thread ===
def update_data():
    global data
    while True:
        for i, ch in enumerate(ads1_channels):
            data[i] = ch.voltage * RATIO
        for i, ch in enumerate(ads2_channels):
            data[i + 4] = ch.voltage * RATIO
        time.sleep(1)

threading.Thread(target=update_data, daemon=True).start()

# === Tkinter GUI ===
root = tk.Tk()
root.title("ADS1015 + MCP23017 GUI")

main_frame = ttk.Frame(root, padding=10)
main_frame.grid(row=0, column=0)

ads_frame = ttk.Frame(main_frame, padding=10)
ads_frame.grid(row=0, column=0)

mcp_frame = ttk.Frame(main_frame, padding=10)
mcp_frame.grid(row=0, column=1)

# === ADS1015 GUI ===
ads_labels = []
for i in range(8):
    label = ttk.Label(ads_frame, text=f"Channel {i}: --- V", font=("Arial", 12))
    label.grid(row=i, column=0, sticky=tk.W)
    ads_labels.append(label)

fig = Figure(figsize=(5, 3), dpi=100)
ax = fig.add_subplot(111)
bars = ax.bar(range(8), data)
ax.set_ylim(0, 30)
ax.set_ylabel("Voltage (V)")
ax.set_title("ADS1015 Voltages")
ax.set_xticks(range(8))
ax.set_xticklabels([f"Ch {i}" for i in range(8)])
canvas = FigureCanvasTkAgg(fig, master=ads_frame)
canvas.draw()
canvas.get_tk_widget().grid(row=0, column=1, rowspan=8)

def refresh_gui():
    for i, label in enumerate(ads_labels):
        label.config(text=f"Channel {i}: {data[i]:.2f} V")
        bars[i].set_height(data[i])
    canvas.draw()
    update_indicators()
    root.after(1000, refresh_gui)

# === MCP23017 GUI ===
a_indicators = []
b_indicators = []

def update_indicators():
    for i, pin in enumerate(a_pins):
        a_indicators[i].config(bg="green" if pin.value else "red")
    for i, pin in enumerate(b_pins):
        b_indicators[i].config(bg="green" if pin.value else "red")

def toggle_pin(pins, idx):
    pins[idx].value = not pins[idx].value
    update_indicators()

def set_pin(pins, idx, state):
    pins[idx].value = state
    update_indicators()

def create_pin_controls(frame, label_prefix, pins, indicators):
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

# === Start GUI Loop ===
root.after(1000, refresh_gui)
root.mainloop()
