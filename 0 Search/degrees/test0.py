#!/usr/bin/env python3
import sys

def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"
    print(sys.argv[0], sys.argv[1])
    print(directory)
    source = input("Name: ")
    print(source)

if __name__ == "__main__":
    main()
