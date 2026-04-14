"""
process_finder.py
=================
Uses psutil to find which process currently has an open handle
on the given file path.

Note: On Windows, enumerating open file handles for ALL processes
requires elevated (Administrator) privileges.
"""

import psutil
from logger_config import get_logger
from typing import Tuple, Optional

logger = get_logger()


def find_culprit_process(filepath: str) -> Tuple[Optional[int], Optional[str]]:
    """
    Iterate all running processes and check their open file handles
    to find which process is touching `filepath`.

    Returns:
        (pid, process_name) if found, else (None, None)
    """
    target = filepath.lower()

    for proc in psutil.process_iter(attrs=["pid", "name"]):
        try:
            open_files = proc.open_files()
            for f in open_files:
                if f.path.lower() == target:
                    return proc.info["pid"], proc.info["name"]
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # Process disappeared or we lack permission — skip it
            continue
        except Exception as exc:
            logger.debug(f"  Error checking PID {proc.pid}: {exc}")
            continue

    # Fallback: try to match by recently-modified handles (heuristic)
    return _fallback_find(target)


def _fallback_find(target: str) -> Tuple[Optional[int], Optional[str]]:
    """
    Secondary heuristic: find the most recently created/modified process
    that has any files open in the same directory as the target.
    Used when the file handle has already been released.
    """
    target_dir = target.rsplit("\\", 1)[0] if "\\" in target else target

    candidates = []
    for proc in psutil.process_iter(attrs=["pid", "name", "create_time"]):
        try:
            open_files = proc.open_files()
            for f in open_files:
                if target_dir in f.path.lower():
                    candidates.append((proc.info["create_time"], proc.info["pid"], proc.info["name"]))
                    break
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    if candidates:
        # Pick the process most recently launched (most likely the threat)
        candidates.sort(reverse=True)
        _, pid, name = candidates[0]
        logger.debug(f"  Fallback identified: {name} (PID {pid})")
        return pid, name

    return None, None
