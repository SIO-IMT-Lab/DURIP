# IMT Lab: DURIP Project

All code and documentation for the DURIP Project at the SIO IMT Lab.

## Repository Structure

```text
.
├── AML/                   # Serial logger for AML water quality sensor
├── Ethernet_Relay_Switch/ # TCP utilities and GUI for Ethernet relay
├── IO_Control/            # ADS1015 & MCP23017 I2C utilities and GUIs
├── LabVIEW_Source/        # LabVIEW projects and shared VIs for cDAQ
├── Transmissometer/       # Serial logger for Seabird transmissometer
└── webapps/               # FastAPI web applications and shared scheduling logic
```

```mermaid
graph TD
    subgraph Sensors
        AML
        TX[Transmissometer]
        cDAQ
        Subnero
        FSO
    end
    Scheduler[Schedule Manager\n(webapps/shared)]
    Client[Web Client]
    Admin[Admin Dashboard]
    Client -->|HTTP| Scheduler
    Admin -->|HTTP + Auth| Scheduler
    Scheduler -->|cron jobs| Sensors
    Scheduler --> Files[Schedule Files]
```

## Web Applications

Two FastAPI-based web applications live under `webapps/`:

- `webapps/client` – a user-facing scheduler that leverages shared services.
- `webapps/admin` – a secured dashboard with HTTP Basic authentication.

Shared assets and scheduling logic reside in `webapps/shared`.

## Task List

- [x] Build a LabVIEW executable that runs on startup
- [x] Implement transmit/receive scheduling from a configuration file
- [x] Provide manual override for immediate transmit
- [ ] Automate upload of Rx files to the DURIP computer
- [ ] Verify contents of transferred binary files
- [ ] Add error-checking to prevent disk overrun or invalid waveforms
- [ ] Expose user-programmable acquisition variables (e.g., sampling rate, gain)

## Notes

- The underwater testbed executes schedules loaded from the DURIP computer.
- Instruments (AML water quality sensor, Seabird transmissometer, subNero modems, FSO, cDAQ) are powered only when needed to conserve energy.
- Serial devices log low-rate data; Ethernet devices expose web servers for command and control.
- The cDAQ transmits specified files, logs received data, then powers down.
- Accurate time synchronization across all nodes is essential for coordinated operation.
