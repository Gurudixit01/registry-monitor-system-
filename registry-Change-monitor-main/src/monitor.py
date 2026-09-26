from __future__ import annotations
import json
import time
from pathlib import Path
from .detector import diff_snapshots
from .registry import snapshot

def append_events(events, output):
    path = Path(output); path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        for event in events:
            handle.write(json.dumps(event, default=str) + "\n")

def monitor(paths, interval, log_path, baseline=None):
    previous = baseline if baseline is not None else snapshot(paths)
    print(f"Monitoring {len(paths)} Registry locations every {interval}s. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(interval)
            current = snapshot(paths)
            events = diff_snapshots(previous, current)
            if events:
                append_events(events, log_path)
                for event in events:
                    print(f"[{event['severity']}] {event['action']} {event['path']} -> {event['name']}")
            previous = current
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")
