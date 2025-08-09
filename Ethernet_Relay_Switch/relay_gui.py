#!/usr/bin/env python3
"""
Dark-themed Tkinter / ttk GUI for a two channel Ethernet relay
"""

import socket
import tkinter as tk
from tkinter import ttk, messagebox

IP, PORT = "192.168.1.100", 6722
TIMEOUT  = 2.0


def send(cmd: bytes) -> str:
    """Send one ASCII frame, return the reply string or '' on error"""
    try:
        with socket.create_connection((IP, PORT), timeout=TIMEOUT) as s:
            s.sendall(cmd)
            return s.recv(16).decode(errors="ignore").strip()
    except OSError as exc:
        messagebox.showerror("Network error", str(exc))
        return ""


class RelayGUI(tk.Tk):
    DARK_BG   = "#2d2d2d"
    LED_ON    = "#00c851"
    LED_OFF   = "#ff4444"

    def __init__(self):
        super().__init__()
        self.title("Ethernet Relay Control")
        self.configure(bg=self.DARK_BG)
        self.resizable(False, False)

        # Style tweaks
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Red.TButton",   foreground="white", background="#d9534f")
        style.map      ("Red.TButton",   background=[("active", "#c9302c")])
        style.configure("Green.TButton", foreground="white", background="#5cb85c")
        style.map      ("Green.TButton", background=[("active", "#449d44")])
        style.configure("Blue.TButton",  foreground="white", background="#428bca")
        style.map      ("Blue.TButton",  background=[("active", "#3071a9")])
        style.configure(".", borderwidth=0)

        # Title
        ttk.Label(self, text="Two Channel Relay",
                  font=("Helvetica", 16, "bold"),
                  foreground="white", background=self.DARK_BG)\
            .grid(row=0, column=0, columnspan=4, pady=(10, 8))

        # Relay 1 widgets
        ttk.Label(self, text="Relay 1", font=("Helvetica", 14),
                  foreground="white", background=self.DARK_BG)\
            .grid(row=1, column=0, padx=10, pady=6)

        ttk.Button(self, text="Close", style="Green.TButton",
                   command=lambda: self.act(b"11"))\
            .grid(row=1, column=1, padx=6)
        ttk.Button(self, text="Open",  style="Red.TButton",
                   command=lambda: self.act(b"21"))\
            .grid(row=1, column=2, padx=6)

        self.led1 = tk.Label(self, width=2, bg=self.LED_OFF)
        self.led1.grid(row=1, column=3, padx=12)

        # Relay 2 widgets
        ttk.Label(self, text="Relay 2", font=("Helvetica", 14),
                  foreground="white", background=self.DARK_BG)\
            .grid(row=2, column=0, padx=10, pady=6)

        ttk.Button(self, text="Close", style="Green.TButton",
                   command=lambda: self.act(b"12"))\
            .grid(row=2, column=1, padx=6)
        ttk.Button(self, text="Open",  style="Red.TButton",
                   command=lambda: self.act(b"22"))\
            .grid(row=2, column=2, padx=6)

        self.led2 = tk.Label(self, width=2, bg=self.LED_OFF)
        self.led2.grid(row=2, column=3, padx=12)

        # Read state button
        ttk.Button(self, text="Read status", style="Blue.TButton", width=28,
                   command=self.read_status)\
            .grid(row=3, column=0, columnspan=4, pady=(10, 4))

        # Raw reply display
        self.reply_lbl = ttk.Label(self, text="--------",
                                   foreground="white", background=self.DARK_BG,
                                   font=("Consolas", 12))
        self.reply_lbl.grid(row=4, column=0, columnspan=4, pady=(0, 10))

        # start polling
        self.after(500, self.read_status)

    # helpers
    def act(self, cmd: bytes):
        send(cmd)
        self.after(150, self.read_status)

    def read_status(self):
        reply = send(b"00")
        if len(reply) == 8:
            self.reply_lbl.configure(text=reply)
            self.led1.configure(bg=self.LED_ON if reply[0] == "1" else self.LED_OFF)
            self.led2.configure(bg=self.LED_ON if reply[1] == "1" else self.LED_OFF)
        self.after(1000, self.read_status)


if __name__ == "__main__":
    RelayGUI().mainloop()

