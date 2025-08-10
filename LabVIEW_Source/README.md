# LabVIEW Source

This directory organizes the LabVIEW projects and supporting files used for DURIP cDAQ development.  The content has been regrouped from multiple legacy backups into a consistent structure.

## Directory Layout

- `projects/` – Individual LabVIEW projects.  Each subfolder contains a `.lvproj` file along with its associated `.aliases` and `.lvlps` configuration files.  Project‑specific VIs live alongside the project files.
- `vis/` – Stand‑alone VIs that are shared across projects.
  - `common/` – VIs reused by many projects such as shutdown handling and clock synchronization.
  - `standalone/` – Utility or example VIs not tied to a specific project.
- `docs/` – Notes and miscellaneous documentation gathered from the original backups.
- `data/` – Captured data files (e.g., binary captures from file‑transfer tests).
- `library/` – Shared LabVIEW libraries.

## Projects

Below is a brief description of each project folder.

| Project folder | Description |
| -------------- | ----------- |
| `ai_ao_sync_clocks` | Test bench for synchronizing analog input/output clocks. Includes `test_082021.vi`. |
| `cdaq_control_121423` | Control software for the cDAQ chassis as of 2023‑12‑14. Uses `test_loop.vi` and shared shutdown logic. |
| `cdaq_project_template` | Template project for starting new cDAQ applications. |
| `cdaq_test` | Basic cDAQ test application including `cdaq_test.vi` and shared shutdown handling. |
| `control_082021` | Early DURIP control project from August 2021. |
| `development` | Miscellaneous development sandbox used during early experiments. |
| `getting_started` | Starter examples for voltage acquisition/output using the cDAQ. Contains several sample voltage VIs. |
| `ni9262_waveform_test` | Waveform generation tests targeting the NI‑9262 module. |
| `ni9775_acquisition_test` | Acquisition tests for the NI‑9775 module. |
| `shutdown_test_112023` | November 2023 cDAQ shutdown testing. |
| `shutdown_test_121323` | December 2023 cDAQ shutdown testing. |
| `standalone_121923` | Stand‑alone Tx/Rx application created December 2023. Uses `cdaq_txrx.vi` along with shared scheduling and clock sync VIs. |
| `standalone_test_091721` | Stand‑alone cDAQ test from September 2021 including the `cdaq_blinky.vi` demo. |
| `testing_082321` | August 2021 bench testing; exercises scheduling and clock sync utilities. |
| `test_082021` | Minimal test harness from August 2021 using shared clock synchronization logic. |
| `test_tcp_120423` | Simple TCP client test project including `tcp_client_test.vi`. |

## Common VIs

Shared VIs are located in `vis/common/`:

- `bench_scheduling.vi` – Utility for bench test scheduling.
- `shutdown.vi` – Graceful shutdown routine used across projects.
- `sync_clocks.vi` – Synchronizes system and module clocks.

Additional standalone example VIs live under `vis/standalone/` such as `cdaq_sync_test.vi` and `cdaq_vi_vo_sync_clocks.vi`.

## Usage

Open any `.lvproj` file within its project folder to work with that project in LabVIEW. Ensure that the `vis/common` directory remains relative to the projects so shared VIs resolve correctly.

