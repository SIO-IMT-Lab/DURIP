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

# Constants
RATIO = 24 / 2.17  # volts / volts

# Initialize I2C bus
i2c = busio.I2C(board.SCL, board.SDA)
ads1 = ADS1015(i2c, address=0x48)
ads2 = ADS1015(i2c, address=0x49)
ads1_channels = [AnalogIn(ads1, ch) for ch in [0,1,2,3]]
ads2_channels = [AnalogIn(ads2, ch) for ch in [0,1,2,3]]

# Data storage
data = [0] * 8

# GUI update function
def update_data():
    global data
    while True:
        for i, ch in enumerate(ads1_channels):
            data[i] = ch.voltage * RATIO
        for i, ch in enumerate(ads2_channels):
            data[i + 4] = ch.voltage * RATIO
        time.sleep(1)

# Start data thread
thread = threading.Thread(target=update_data, daemon=True)
thread.start()

# Tkinter GUI setup
root = tk.Tk()
root.title("Live ADS1015 Readings")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

labels = []
for i in range(8):
    label = ttk.Label(frame, text=f"Channel {i}: --- V", font=("Arial", 14))
    label.grid(row=i, column=0, sticky=tk.W)
    labels.append(label)

# Matplotlib figure
fig = Figure(figsize=(6, 4), dpi=100)
ax = fig.add_subplot(111)
bars = ax.bar(range(8), data)
ax.set_ylim(0, 30)
ax.set_ylabel("Voltage (V)")
ax.set_title("Scaled ADS1015 Voltages")
ax.set_xticks(range(8))
ax.set_xticklabels([f"Ch {i}" for i in range(8)])

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().grid(row=0, column=1, rowspan=8)

# GUI refresh function
def refresh_gui():
    for i, label in enumerate(labels):
        label.config(text=f"Channel {i}: {data[i]:.2f} V")
        bars[i].set_height(data[i])
    canvas.draw()
    root.after(1000, refresh_gui)

root.after(1000, refresh_gui)
root.mainloop()
