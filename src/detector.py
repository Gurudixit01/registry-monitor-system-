from __future__ import annotations
import re
from datetime import datetime, timezone

EXECUTABLE_RE = re.compile(r'\.(exe|dll|bat|cmd|ps1|vbs|js)(["\s]|$)', re.I)

def classify_change(path, name, value):
    text = str(value)
    reasons = []
    if "\\Run" in path or "\\RunOnce" in path:
        if EXECUTABLE_RE.search(text):
            reasons.append("Executable autorun entry")
    lowered = f"{path}\\{name}\\{text}".lower()
    terms = ("disableantispyware", "disableantivirus", "disablefirewall", "disabledefender", "enablelua", "policies\\system")
    if any(term in lowered for term in terms):
        reasons.append("Security-policy or protection-related Registry indicator")
    if any(term in lowered for term in ("powershell", "wscript", "cscript", "mshta")):
        reasons.append("Script/interpreter execution indicator")
    return (reasons, "HIGH") if reasons else (["Registry state changed"], "LOW")

def diff_snapshots(old, new):
    events = []
    for key_path in sorted(set(old) | set(new)):
        old_values, new_values = old.get(key_path, {}), new.get(key_path, {})
        if "__error__" in old_values or "__error__" in new_values:
            continue
        for name in sorted(set(old_values) | set(new_values)):
            if name not in old_values: action = "ADD"
            elif name not in new_values: action = "DELETE"
            elif old_values[name] != new_values[name]: action = "MODIFY"
            else: continue
            old_value = old_values.get(name, {}).get("value")
            new_value = new_values.get(name, {}).get("value")
            reasons, severity = classify_change(key_path, name, new_value)
            events.append({"timestamp": datetime.now(timezone.utc).isoformat(), "action": action,
                           "path": key_path, "name": name, "old_value": old_value,
                           "new_value": new_value, "severity": severity, "reasons": reasons})
    return events
