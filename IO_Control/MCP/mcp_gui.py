import tkinter as tk
from tkinter import ttk
import board
import busio
import digitalio
from adafruit_mcp230xx.mcp23017 import MCP23017

# Initialize I2C and MCP23017
i2c = busio.I2C(board.SCL, board.SDA)
mcp = MCP23017(i2c, address=0x20)

# Setup A0–A7 and B0–B7 as outputs
a_pins = []
b_pins = []
for pin_num in range(8):
    a_pin = mcp.get_pin(pin_num)  # A0–A7 → 0–7
    b_pin = mcp.get_pin(pin_num + 8)  # B0–B7 → 8–15
    a_pin.direction = digitalio.Direction.OUTPUT
    b_pin.direction = digitalio.Direction.OUTPUT
    a_pin.value = False
    b_pin.value = False
    a_pins.append(a_pin)
    b_pins.append(b_pin)

# === GUI Setup ===
root = tk.Tk()
root.title("MCP23017 A & B Pins Controller")
root.geometry("600x500")
root.configure(bg="#2c3e50")

header = tk.Label(root, text="MCP23017 A0–A7 and B0–B7 Control Panel", font=("Arial", 18, "bold"), bg="#2c3e50", fg="white")
header.pack(pady=10)

main_frame = ttk.Frame(root, padding=10)
main_frame.pack()

# Hold indicators
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

def show_status():
    status_lines = []
    status_lines += [f"A{i}: {'HIGH' if p.value else 'LOW'}" for i, p in enumerate(a_pins)]
    status_lines += [f"B{i}: {'HIGH' if p.value else 'LOW'}" for i, p in enumerate(b_pins)]
    status_text = "\n".join(status_lines)
    status_window = tk.Toplevel(root)
    status_window.title("Pin Status")
    tk.Label(status_window, text=status_text, font=("Courier", 12), justify="left").pack(padx=20, pady=20)

def create_pin_controls(frame, label_prefix, pins, indicators):
    section = ttk.LabelFrame(frame, text=f"{label_prefix} Pins", padding=10)
    section.pack(side="left", padx=10)

    for i in range(8):
        row = ttk.Frame(section, padding=5)
        row.pack(anchor="w")

        label = ttk.Label(row, text=f"{label_prefix}{i}", width=4)
        label.pack(side="left")

        indicator = tk.Label(row, text=" ", bg="red", width=2, height=1, relief="groove")
        indicator.pack(side="left", padx=5)
        indicators.append(indicator)

        btn_toggle = ttk.Button(row, text="Toggle", command=lambda idx=i: toggle_pin(pins, idx))
        btn_toggle.pack(side="left", padx=2)

        btn_on = ttk.Button(row, text="ON", command=lambda idx=i: set_pin(pins, idx, True))
        btn_on.pack(side="left", padx=2)

        btn_off = ttk.Button(row, text="OFF", command=lambda idx=i: set_pin(pins, idx, False))
        btn_off.pack(side="left", padx=2)

# Create A and B pin controls
create_pin_controls(main_frame, "A", a_pins, a_indicators)
create_pin_controls(main_frame, "B", b_pins, b_indicators)

# Bottom buttons
bottom_frame = ttk.Frame(root, padding=10)
bottom_frame.pack()

status_btn = ttk.Button(bottom_frame, text="Show Status", command=show_status)
status_btn.pack(side="left", padx=10)

exit_btn = ttk.Button(bottom_frame, text="Exit", command=root.quit)
exit_btn.pack(side="left", padx=10)

# Initialize indicators
update_indicators()

# Run the GUI loop
root.mainloop()
