import sys

def parse_log(file):
    try:
        with open(file, "r") as file:
            lines = file.readlines()
        return lines
    except FileNotFoundError:
        print(f"Error: File {file} not found.")
        sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 analyzer.py <path-to-log-file")
        sys.exit(1)

    log_file = sys.argv[1]

    lines = parse_log(log_file)
    print(f"Successfully parsed {len(lines)} lines.")

    if __name__ == "__main__":
        main()
