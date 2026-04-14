"""
honey_setup.py
==============
Creates the C:\\HoneyTrap directory and plants decoy honey-files.
Files are named with a leading '!' so they appear first in
any alphabetical directory sweep by ransomware.
"""

import os
from pathlib import Path
from logger_config import get_logger

logger = get_logger()

# ── Configuration ──────────────────────────────────────────────────────────────
HONEY_TRAP_DIR = Path(r"C:\HoneyTrap")
NUM_HONEY_FILES = 5
HONEY_FILE_PREFIX = "!ARACHNE_HONEY_"
HONEY_FILE_EXT = ".txt"
SENTINEL_CONTENT = (
    "ARACHNE SENTINEL FILE\n"
    "DO NOT MODIFY — THIS FILE IS A SECURITY TRIPWIRE.\n"
    "Any process that modifies this file will be identified and terminated.\n"
)

SAFE_LIST: set[str] = {
    # Add trusted process names here (lowercase)
    "explorer.exe",
    "python.exe",       # remove this in production!
    "pythonw.exe",
    "code.exe",
    "notepad.exe",
    "system",
}


def setup_honey_trap() -> None:
    """Create the honey-trap directory and plant sentinel files."""
    HONEY_TRAP_DIR.mkdir(parents=True, exist_ok=True)
    logger.info(f"Honey-trap directory ensured: {HONEY_TRAP_DIR}")

    for i in range(1, NUM_HONEY_FILES + 1):
        filename = f"{HONEY_FILE_PREFIX}{i:03d}{HONEY_FILE_EXT}"
        filepath = HONEY_TRAP_DIR / filename
        if not filepath.exists():
            filepath.write_text(SENTINEL_CONTENT, encoding="utf-8")
            logger.info(f"  [+] Planted: {filename}")
        else:
            logger.info(f"  [=] Already exists: {filename}")

    logger.info(f"Honey-trap ready with {NUM_HONEY_FILES} sentinel files.")
