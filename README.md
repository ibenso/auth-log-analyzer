# Analyseverktøy for autentiseringslogger
# auth-log-analyzer
A Python-based tool for analyzing Linux authentication logs (`/var/log/auth.log`).  
The analyzer detects suspicious activity such as brute-force attempts, invalid user logins, night-time activity, successful logins, and generates a clean, structured security report.

## Features
- Count failed login attempts per IP  
- Detect invalid user attempts  
- Flag night-time activity (00–05)  
- Extract successful logins with timestamp and IP  
- Generate a clean report

## Project structure
auth-log-analyzer/
│
├── src/
│ └── analyzer.py # Main analysis script
│
├── sample_logs/
│ └── auth.log # Sample authentication log
│
├── results/
│ └── report.txt # Generated report
│
└── README.md

## Usage
python3 src/analyzer.py sample_logs/auth.log