import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 analyzer.py <path-to-log-file")
        sys.exit(1)

    log_file = sys.argv[1]

    try:
        with open(log_file, "r") as file:
            lines = file.readlines()
        print(f"Read {len(lines)} lines from {log_file}")
    except FileNotFoundError:
        print(f"Error: File {log_file} not found.")
        sys.exit(1)

    if __name__ == "__main__":
        main()