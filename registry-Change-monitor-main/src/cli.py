import argparse, json
from .config import Config
from .detector import diff_snapshots
from .monitor import append_events, monitor
from .registry import load_snapshot, save_snapshot, snapshot
from .reporting import export_csv

def main():
    parser = argparse.ArgumentParser(description="Defensive Windows Registry monitoring toolkit")
    parser.add_argument("--config")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("baseline"); p.add_argument("--output", default="data/baseline.json")
    p = sub.add_parser("check"); p.add_argument("--baseline", default="data/baseline.json"); p.add_argument("--log", default="logs/registry_changes.jsonl")
    p = sub.add_parser("monitor"); p.add_argument("--baseline"); p.add_argument("--interval", type=int); p.add_argument("--log", default="logs/registry_changes.jsonl")
    p = sub.add_parser("report"); p.add_argument("--input", default="logs/registry_changes.jsonl"); p.add_argument("--output", default="logs/registry_report.csv")
    args = parser.parse_args(); config = Config.load(args.config)
    if args.command == "baseline": save_snapshot(snapshot(config.registry_paths), args.output); print(f"Baseline saved to {args.output}")
    elif args.command == "check":
        events = diff_snapshots(load_snapshot(args.baseline), snapshot(config.registry_paths)); append_events(events, args.log); print(json.dumps(events, indent=2, default=str))
    elif args.command == "monitor": monitor(config.registry_paths, args.interval or config.poll_interval, args.log, load_snapshot(args.baseline) if args.baseline else None)
    elif args.command == "report": export_csv(args.input, args.output); print(f"Report saved to {args.output}")

if __name__ == "__main__": main()
