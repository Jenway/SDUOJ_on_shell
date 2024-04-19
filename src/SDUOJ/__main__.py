# __main__.py
import sys
from . import ojd, uploadAns as oju

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m SDUOJ -[ojd|oju]")
        return

    command = sys.argv[1]
    if command == '-ojd':
        ojd.ojd()
    elif command == '-oju':
        oju.oju()
    else:
        print(f"Unknown command: {command}")
        print("Usage: python -m SDUOJ -[ojd|oju]")
        print("Hints: add an alias like ojd='python -m SDUOJ -ojd' to your shell profile if you like.")

if __name__ == "__main__":
    main()