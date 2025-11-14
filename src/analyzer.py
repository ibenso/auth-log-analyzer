import sys
import re
from collections import defaultdict
from datetime import datetime

def extract_timestamp(line):
    match = re.match(r"([A-Z][a-z]{2}\s+\d+\s+\d+:\d+:\d+)", line)
    if not match:
        return None, None
    
    timestamp_str = match.group(1)

    datetime = datetime.strptime("2025" + timestamp_str, "%Y %b %d %H:%M:%S")
    return datetime, datetime.hour

def parse_log(file):
    failed_per_ip = defaultdict(int)
    invalid_users = defaultdict(int)

    try:
        with open(file, "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Error: File {file} not found.")
        sys.exit(1)

    for line in lines:
        line = line.strip()

        if "Failed password" in line:

            ip_match = re.search(r"from ([0-9.]+)", line)
            if ip_match:
                ip = ip_match.group(1)
                failed_per_ip[ip] += 1

            invalid_match = re.search(r"Failed password for invalid user (\w+)", line)
            if invalid_match:
                user = invalid_match.group(1)
                invalid_users[user] += 1
            
    return failed_per_ip, invalid_users

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 analyzer.py <path-to-log-file")
        sys.exit(1)

    log_file = sys.argv[1]
    failed_per_ip, invalid_users = parse_log(log_file)

    print("Failed login attempts per IP:")
    for ip, count in failed_per_ip.items():
        print(f"{ip}: {count}")

    print("\nInvalid user attempts:")
    for user, count in invalid_users.items():
        print(f"{user}: {count}")

if __name__ == "__main__":
    main()
