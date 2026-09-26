import unittest
from src.detector import diff_snapshots

class DetectorTests(unittest.TestCase):
    def test_added_autorun(self):
        old = {"HKCU\\Software\\Run": {}}
        new = {"HKCU\\Software\\Run": {"Demo": {"value": r"C:\\Temp\\demo.exe", "type": 1}}}
        events = diff_snapshots(old, new)
        self.assertEqual(events[0]["action"], "ADD")
        self.assertEqual(events[0]["severity"], "HIGH")
    def test_modified_value(self):
        old = {"HKCU\\Software\\Run": {"Demo": {"value": "old", "type": 1}}}
        new = {"HKCU\\Software\\Run": {"Demo": {"value": "new", "type": 1}}}
        self.assertEqual(diff_snapshots(old, new)[0]["action"], "MODIFY")
    def test_unchanged(self):
        state = {"HKCU\\Software\\Run": {"Demo": {"value": "same", "type": 1}}}
        self.assertEqual(diff_snapshots(state, state), [])

if __name__ == "__main__": unittest.main()
