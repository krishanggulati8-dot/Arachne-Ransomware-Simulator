🕸️ Arachne: A Ransomware Defense Simulator
📋 Overview
Arachne is a proactive ransomware defense mechanism designed to detect and neutralize cryptographic threats in real-time. Built on the principle of Deceptive Security, it utilizes a Honey-file (Tripwire) system to monitor sensitive directories. The tool identifies unauthorized file interactions and autonomously terminates malicious processes before they can encrypt the entire file system.

🛡️ Core Architecture & Logic
Arachne operates by deploying "Honey-files"—decoy documents that act as silent alarms. Under normal operations, these files remain untouched. However, ransomware, which typically scans and encrypts every file in a directory, inevitably triggers these tripwires.

Continuous Surveillance: Utilizing the watchdog library, Arachne maintains a high-fidelity monitor on the designated trap directory (C:\HoneyTrap).

Instantaneous Detection: Any file operation (Modification, Renaming, or Deletion) within the trap zone triggers an immediate security event.

Process Forensics: Through the psutil framework, the system captures the Process ID (PID) and Image Name responsible for the file interaction.

Automated Response: The system cross-references the offending process against a Kernel-level Safe List. If the process is unauthorized, Arachne executes a force-kill command to halt the attack.

🚀 Quick Start Guide
1. Prerequisites
Ensure you have Python 3.8+ installed. It is recommended to run this in a Windows environment for full psutil process handle support.

2. Installation
Clone the repository and install the necessary dependencies:

Bash
git clone https://github.com/krishanggulati8-dot/Arachne-Ransomware-Simulator
cd Arachne-Ransomware-Simulator
pip install -r requirements.txt
3. Execution (The Simulation)
To demonstrate the system, follow these steps using two separate terminals:

Terminal 1: The Defender (Run as Administrator)

Bash
python arachne_monitor.py
This initializes the Honey-Trap environment and starts the real-time observer.

Terminal 2: The Attack Simulator

Bash
python fake_ransomware.py
This simulates a cryptographic attack. Watch as Arachne detects the threat and terminates the process instantly.

⚠️ Disclaimer
This software is developed for educational and research purposes only. It serves as a proof-of-concept for behavior-based ransomware detection. The authors are not responsible for any misuse or damage caused by this tool.
