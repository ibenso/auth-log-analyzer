import sys
import re
from collections import defaultdict

def parse_log(file):
    failed_per_ip = defaultdict(int)

    try:
        with open(file, "r") as file:
            lines = file.readlines()
        return lines
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
            
    return failed_per_ip

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 analyzer.py <path-to-log-file")
        sys.exit(1)

    log_file = sys.argv[1]
    failed_per_ip = parse_log(log_file)

    print("Failed login attempts per IP:")
    for ip, count in failed_per_ip.items():
        print(f"{ip}: {count}")

    if __name__ == "__main__":
        main()
