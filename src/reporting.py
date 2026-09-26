from pathlib import Path
import csv, json
FIELDS = ["timestamp","action","path","name","old_value","new_value","severity","reasons"]

def export_csv(input_path, output_path):
    source = Path(input_path)
    if not source.exists(): raise FileNotFoundError(input_path)
    rows = []
    for line in source.read_text(encoding="utf-8").splitlines():
        if line.strip():
            row = json.loads(line); row["reasons"] = "; ".join(row.get("reasons", [])); rows.append(row)
    dest = Path(output_path); dest.parent.mkdir(parents=True, exist_ok=True)
    with dest.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader(); writer.writerows(rows)
