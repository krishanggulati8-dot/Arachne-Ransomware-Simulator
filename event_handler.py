"""
event_handler.py
================
Watchdog FileSystemEventHandler subclass.
Fires on any modification or rename of files inside the honey-trap.
"""

from watchdog.events import FileSystemEventHandler, FileModifiedEvent, FileMovedEvent
from process_finder import find_culprit_process
from honey_setup import SAFE_LIST
from logger_config import get_logger
import psutil

logger = get_logger()


class HoneyFileHandler(FileSystemEventHandler):
    """
    Monitors the honey-trap folder.
    Any modification or rename triggers threat detection.
    """

    def on_modified(self, event):
        if event.is_directory:
            return
        self._handle_threat(event.src_path, event_type="MODIFIED")

    def on_moved(self, event):
        """Fires when a file is renamed (src → dest)."""
        self._handle_threat(
            event.src_path,
            event_type=f"RENAMED → {event.dest_path}",
        )

    def on_created(self, event):
        """Catches cases where ransomware creates a new encrypted copy."""
        if event.is_directory:
            return
        self._handle_threat(event.src_path, event_type="CREATED")

    def on_deleted(self, event):
        if event.is_directory:
            return
        self._handle_threat(event.src_path, event_type="DELETED")

    # ──────────────────────────────────────────────────────────────────────────

    def _handle_threat(self, filepath: str, event_type: str) -> None:
        logger.warning(f"HONEY-FILE TOUCHED | Event: {event_type} | File: {filepath}")

        pid, proc_name = find_culprit_process(filepath)

        if pid is None:
            logger.warning(f"  Could not identify responsible process (may have already exited).")
            return

        logger.warning(f"  Responsible Process: {proc_name} (PID: {pid})")

        # ── Safe-list check ──────────────────────────────────────────────────
        if proc_name.lower() in SAFE_LIST:
            logger.info(f"  Process '{proc_name}' is on the safe-list. No action taken.")
            return

        # ── Kill the process ─────────────────────────────────────────────────
        _terminate_process(pid, proc_name)


def _terminate_process(pid: int, proc_name: str) -> None:
    """Terminate a process by PID and log the outcome."""
    try:
        proc = psutil.Process(pid)
        proc.kill()
        logger.critical(
            f"  ACTION: PROCESS KILLED | Name: {proc_name} | PID: {pid}"
        )
    except psutil.NoSuchProcess:
        logger.warning(f"  Process PID {pid} no longer exists (already terminated?).")
    except psutil.AccessDenied:
        logger.critical(
            f"  ACCESS DENIED: Could not kill {proc_name} (PID {pid}). "
            f"Run Arachne as Administrator."
        )
    except Exception as exc:
        logger.error(f"  Unexpected error killing PID {pid}: {exc}")
