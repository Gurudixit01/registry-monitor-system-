from __future__ import annotations
import json
import platform
import winreg
from pathlib import Path

HIVES = {"HKCU": winreg.HKEY_CURRENT_USER, "HKLM": winreg.HKEY_LOCAL_MACHINE}

def _normalize(value):
    return {"type": "bytes", "value": value.hex()} if isinstance(value, bytes) else value

def read_key(hive_name: str, subkey: str) -> dict:
    if platform.system() != "Windows":
        raise OSError("This project requires Windows.")
    result = {}
    with winreg.OpenKey(HIVES[hive_name], subkey, 0, winreg.KEY_READ) as key:
        index = 0
        while True:
            try:
                name, value, value_type = winreg.EnumValue(key, index)
                result[name] = {"value": _normalize(value), "type": int(value_type)}
                index += 1
            except OSError:
                break
    return result

def snapshot(paths: list[list[str]]) -> dict:
    result = {}
    for hive, subkey in paths:
        identifier = f"{hive}\\{subkey}"
        try:
            result[identifier] = read_key(hive, subkey)
        except FileNotFoundError:
            result[identifier] = {}
        except PermissionError as exc:
            result[identifier] = {"__error__": f"Permission denied: {exc}"}
    return result

def save_snapshot(data, output):
    path = Path(output); path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")

def load_snapshot(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))
