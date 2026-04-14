"""
fake_ransomware.py
==================
⚠  SIMULATION ONLY — FOR TESTING ARACHNE IN A SAFE ENVIRONMENT ⚠

This script mimics the behavior of ransomware:
  1. Scans the honey-trap directory for files.
  2. Attempts to rename each file with a .locked extension.
  3. Attempts to overwrite file content with fake "encrypted" data.

When Arachne is running, it will detect step 2 on the FIRST file
and kill THIS process before it can reach the remaining files —
proving that the honey-file tripwire defense works.

Usage:
  1. Start arachne_monitor.py in one terminal (as Administrator).
  2. Run this script in a second terminal.
  3. Observe Arachne kill this process and log the event.

DO NOT run on a real machine with important data.
Target: C:\\HoneyTrap only.
"""

import os
import time
from pathlib import Path

HONEY_TRAP_DIR = Path(r"C:\HoneyTrap")
FAKE_ENCRYPTED_CONTENT = (
    "X5FGH2KL9MNP3QRS7TUV1WXY4Z0AB6CD8EF\n" * 20
)  # gibberish simulating encryption


def simulate_ransomware():
    print("[FAKE RANSOMWARE] Starting encryption sweep...")
    print(f"[FAKE RANSOMWARE] Targeting directory: {HONEY_TRAP_DIR}\n")

    if not HONEY_TRAP_DIR.exists():
        print("[ERROR] Honey-trap directory does not exist. Run arachne_monitor.py first.")
        return

    files = sorted(HONEY_TRAP_DIR.iterdir())  # alphabetical — hits ! files first

    if not files:
        print("[ERROR] No files found in honey-trap directory.")
        return

    for filepath in files:
        if filepath.is_file():
            locked_path = filepath.with_suffix(filepath.suffix + ".locked")
            print(f"[FAKE RANSOMWARE] Renaming: {filepath.name} → {locked_path.name}")

            try:
                # Step 1: Rename (this is what Arachne catches)
                os.rename(filepath, locked_path)
                print(f"  [+] Renamed successfully.")

                # Step 2: Overwrite with fake encrypted content
                locked_path.write_text(FAKE_ENCRYPTED_CONTENT, encoding="utf-8")
                print(f"  [+] Content overwritten (fake encryption).")

            except PermissionError as e:
                print(f"  [-] Permission denied: {e}")
            except FileNotFoundError as e:
                print(f"  [-] File not found (Arachne may have intervened): {e}")
            except Exception as e:
                print(f"  [-] Unexpected error: {e}")

            time.sleep(0.1)  # small delay between files

    print("\n[FAKE RANSOMWARE] Sweep complete (if you see this, Arachne did NOT stop it!)")


if __name__ == "__main__":
    simulate_ransomware()
