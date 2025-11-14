import sys
import re
from collections import defaultdict
from datetime import datetime

def extract_timestamp(line):
    match = re.match(r"([A-Z][a-z]{2}\s+\d+\s+\d+:\d+:\d+)", line)
    if not match:
        return None, None
    
    timestamp_str = match.group(1)

    dt = datetime.strptime("2025 " + timestamp_str, "%Y %b %d %H:%M:%S")
    return dt, dt.hour

def parse_log(file):
    failed_per_ip = defaultdict(int)
    invalid_users = defaultdict(int)
    night_activity = []
    successful_logins = []

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

            dt, hour = extract_timestamp(line)
            if hour is not None and hour < 6:
                night_activity.append(line)

        if "Accepted password" in line:
            user_match = re.search(r"Accepted password for (\w+)", line)
            ip_match = re.search(r"from ([0-9.]+)", line)
            dt, hour = extract_timestamp(line)

            if user_match and ip_match:
                user = user_match.group(1)
                ip = ip_match.group(1)

                successful_logins.append({
                    "timestamp": dt,
                    "user": user,
                    "ip": ip
                })
            
    return failed_per_ip, invalid_users, night_activity, successful_logins

def generate_report(output_path, failed_per_ip, invalid_users, night_activity, succesful_logins):
    with open(output_path, "w") as report:
        report.write("---Authentication Log Analysis Report---\n\n")
        
        report.write("Failed login attempts per IP:\n")
        for ip, count in failed_per_ip.items():
            report.write(f"{ip}: {count}\n")
        report.write("\n")
        
        report.write("Invalid user attempts:\n")
        for user, count in invalid_users.items():
            report.write(f"{user}: {count}\n")
        report.write("\n")

        report.write("Night-time activity (00–05):\n")
        for entry in night_activity:
            report.write(f"{entry}\n")
        report.write("\n")

        report.write("Successful logins:\n")
        for entry in succesful_logins:
            ts = entry["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
            user = entry["user"]
            ip = entry["ip"]
            report.write(f"{ts} - User '{user}' logged in from {ip}\n")
        report.write("\n")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 analyzer.py <path-to-log-file")
        sys.exit(1)

    log_file = sys.argv[1]
    failed_per_ip, invalid_users, night_activity, successful_logins = parse_log(log_file)

    print("Failed login attempts per IP:")
    for ip, count in failed_per_ip.items():
        print(f"{ip}: {count}")

    print("\nInvalid user attempts:")
    for user, count in invalid_users.items():
        print(f"{user}: {count}")

    print("\nNight-time activity (00–05):")
    for entry in night_activity:
        print(entry)

    print("\nSuccessful logins:")
    for entry in successful_logins:
        ts = entry["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
        print(f"{ts} - User '{entry['user']}' logged in from {entry['ip']}")

    output_file = "results/report.txt"
    generate_report(output_file, failed_per_ip, invalid_users, night_activity, successful_logins)

if __name__ == "__main__":
    main()
