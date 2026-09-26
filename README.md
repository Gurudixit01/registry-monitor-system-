# Windows Registry Change Monitoring System

A cybersecurity tool that monitors critical Windows Registry locations, detects suspicious modifications, generates alerts, and produces detailed reports for analysis.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Monitored Registry Keys](#monitored-registry-keys)
- [Example Workflow](#example-workflow)
- [Project Objectives](#project-objectives)

## Overview

The system takes a snapshot of the Windows Registry, compares it against later states, and flags added, modified, or deleted values. It focuses on locations commonly abused by malware for persistence, such as autorun keys, and on security-related settings like Windows Defender, firewall, and UAC policies.

## Features

- **Registry baseline creation:** capture a known-good snapshot of the registry
- **Registry integrity verification:** compare the current state against the baseline
- **Real-time change monitoring:** continuous, periodic snapshot comparison
- **Autorun persistence detection:** watch `Run` and `RunOnce` keys
- **Malware-like behavior detection:** flag suspicious changes with a severity and reason
- **Alert generation:** alerts and logs for every detected change
- **CSV report generation:** export all detected events for analysis

## Project Structure

```text
windows-registry/
├── src/
│   ├── cli.py         # Command-line entry point
│   ├── config.py      # Monitored keys and settings
│   ├── detector.py    # Change and suspicious-behavior detection
│   ├── monitor.py     # Continuous monitoring engine
│   ├── registry.py    # Registry reading and snapshot logic
│   └── reporting.py   # CSV report generation
├── data/              # Baseline snapshot (baseline.json)
├── logs/              # Alerts, logs, and reports
└── tests/             # Test suite
```

## Installation

**1. Clone the repository**

```shell
git clone https://github.com/Gurudixit01/windows-registry.git
cd windows-registry
```

**2. Install dependencies**

```shell
pip install -r requirements.txt
```

## Usage

All commands are run through the CLI module:

| Command | Purpose | Output |
|---------|---------|--------|
| `python -m src.cli baseline` | Create a baseline snapshot | `data/baseline.json` |
| `python -m src.cli check` | Run an integrity check against the baseline | Console results |
| `python -m src.cli monitor` | Start continuous monitoring | Alerts and logs |
| `python -m src.cli report` | Generate a security report | `logs/registry_report.csv` |

### 1. Create a Baseline Snapshot

Captures the current registry state and saves it for future comparison.

```shell
python -m src.cli baseline
```

Output: `data/baseline.json`

### 2. Run an Integrity Check

Compares the current registry state against the saved baseline.

```shell
python -m src.cli check
```

Detects:

- Added registry values
- Modified registry values
- Deleted registry values

### 3. Start Continuous Monitoring

Launches the monitoring engine.

```shell
python -m src.cli monitor
```

The system:

1. Reads the monitored registry keys.
2. Creates periodic snapshots.
3. Compares the current snapshot with the previous one.
4. Detects changes.
5. Generates alerts and logs.

Default monitoring interval: **10 seconds**

### 4. Generate a Security Report

Generates a CSV report containing all detected events.

```shell
python -m src.cli report
```

Output: `logs/registry_report.csv`

| Column | Description |
|--------|-------------|
| Timestamp | When the change was detected |
| Registry Path | Location of the changed value |
| Change Type | Added, modified, or deleted |
| Old Value | Value before the change |
| New Value | Value after the change |
| Severity | Severity rating of the event |
| Detection Reason | Why the change was flagged |

## Monitored Registry Keys

### Autorun Locations

```text
HKCU\Software\Microsoft\Windows\CurrentVersion\Run
HKCU\Software\Microsoft\Windows\CurrentVersion\RunOnce
HKLM\Software\Microsoft\Windows\CurrentVersion\Run
HKLM\Software\Microsoft\Windows\CurrentVersion\RunOnce
```

### Security-Related Locations

- Windows Defender policies
- Firewall configuration
- Winlogon configuration
- UAC policies

## Example Workflow

1. **Create the baseline:**

   ```shell
   python -m src.cli baseline
   ```

2. **Start monitoring:**

   ```shell
   python -m src.cli monitor
   ```

3. **Make a registry change** (for example, add a new value under a `Run` key).

4. **Review the alert:** the system detects the modification and generates an alert.

5. **Generate the final report:**

   ```shell
   python -m src.cli report
   ```

## Project Objectives

- Monitor autorun registry keys for persistence mechanisms.
- Detect malware-like registry changes.
- Provide a registry integrity checker using baseline comparison.
- Deliver real-time or scheduled alerts.
- Generate detailed registry change reports.
