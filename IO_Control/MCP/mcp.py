import time
import board
import busio
import digitalio

from adafruit_mcp230xx.mcp23017 import MCP23017

# Initialize I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# === MCP23017 at address 0x20 ===
mcp = MCP23017(i2c, address=0x20)

# Set up A pins as outputs (A0-A7)
pins = []
for pin_num in range(8):
    pin = mcp.get_pin(pin_num)  # 0-7 are A0-A7
    pin.direction = digitalio.Direction.OUTPUT
    pin.value = False  # start LOW
    pins.append(pin)

print("MCP23017 A pins (A0–A7) set as outputs.")
print("Type commands like: set A0 on, set A3 off, toggle A2, status, exit")

def get_pin_index(name):
    if name.upper().startswith("A"):
        idx = int(name[1:])
        if 0 <= idx <= 7:
            return idx
    return None

try:
    while True:
        command = input(">>> ").strip().lower()
        if command == "exit":
            print("Exiting...")
            break
        elif command == "status":
            for i, pin in enumerate(pins):
                print(f"A{i}: {'HIGH' if pin.value else 'LOW'}")
        elif command.startswith("set "):
            parts = command.split()
            if len(parts) == 3:
                pin_name, state = parts[1], parts[2]
                idx = get_pin_index(pin_name)
                if idx is not None and state in ["on", "off"]:
                    pins[idx].value = True if state == "on" else False
                    print(f"Set A{idx} {'HIGH' if pins[idx].value else 'LOW'}")
                else:
                    print("Invalid command. Example: set A0 on")
            else:
                print("Invalid command format. Example: set A0 on")
        elif command.startswith("toggle "):
            parts = command.split()
            if len(parts) == 2:
                pin_name = parts[1]
                idx = get_pin_index(pin_name)
                if idx is not None:
                    pins[idx].value = not pins[idx].value
                    print(f"Toggled A{idx} to {'HIGH' if pins[idx].value else 'LOW'}")
                else:
                    print("Invalid pin. Example: toggle A2")
            else:
                print("Invalid command format. Example: toggle A2")
        else:
            print("Unknown command. Available: set, toggle, status, exit")

except KeyboardInterrupt:
    print("\nExiting cleanly...")
