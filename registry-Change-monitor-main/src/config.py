from dataclasses import dataclass, field
from pathlib import Path
import json

DEFAULT_PATHS = [
    ["HKCU", r"Software\Microsoft\Windows\CurrentVersion\Run"],
    ["HKCU", r"Software\Microsoft\Windows\CurrentVersion\RunOnce"],
    ["HKLM", r"Software\Microsoft\Windows\CurrentVersion\Run"],
    ["HKLM", r"Software\Microsoft\Windows\CurrentVersion\RunOnce"],
    ["HKLM", r"SOFTWARE\Policies\Microsoft\Windows Defender"],
    ["HKLM", r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System"],
    ["HKLM", r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer"],
    ["HKLM", r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon"],
    ["HKLM", r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options"],
    ["HKLM", r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Drivers32"],
    ["HKLM", r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Windows"],
    ["HKLM", r"SYSTEM\CurrentControlSet\Services"],
    ["HKLM", r"SYSTEM\CurrentControlSet\Control\Session Manager"],
]

@dataclass
class Config:
    poll_interval: int = 10
    registry_paths: list = field(default_factory=lambda: DEFAULT_PATHS.copy())

    @classmethod
    def load(cls, path=None):
        if not path:
            return cls()
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls(int(data.get("poll_interval", 10)), data.get("registry_paths", DEFAULT_PATHS))
