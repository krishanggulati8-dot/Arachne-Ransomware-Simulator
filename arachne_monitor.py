"""
arachne_monitor.py
==================
Arachne: Ransomware Defense Simulator — Main Entry Point
Author  : [Your Name]
Project : Arachne
"""

import time
import sys
from watchdog.observers import Observer
from honey_setup import setup_honey_trap, HONEY_TRAP_DIR
from event_handler import HoneyFileHandler
from logger_config import get_logger

logger = get_logger()

BANNER = r"""
    _                     _
   / \   _ __ __ _  ___| |__  _ __   ___
  / _ \ | '__/ _` |/ __| '_ \| '_ \ / _ \
 / ___ \| | | (_| | (__| | | | | | |  __/
/_/   \_\_|  \__,_|\___|_| |_|_| |_|\___|

  Ransomware Defense Simulator v1.0
  Honey-File Tripwire System
  ----------------------------------------
"""

def main():
    print(BANNER)

    # Step 1: plant honey-files
    setup_honey_trap()
    logger.info(f"Honey-trap active at: {HONEY_TRAP_DIR}")

    # Step 2: set up watchdog observer
    event_handler = HoneyFileHandler()
    observer = Observer()
    observer.schedule(event_handler, path=str(HONEY_TRAP_DIR), recursive=False)
    observer.start()
    logger.info("Observer started. Monitoring for threats... (Ctrl+C to stop)")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Shutdown signal received. Stopping observer...")
        observer.stop()

    observer.join()
    logger.info("Arachne stopped cleanly.")
    sys.exit(0)


if __name__ == "__main__":
    main()
