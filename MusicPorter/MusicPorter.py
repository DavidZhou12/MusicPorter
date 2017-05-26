import os, sndhdr, sys
import eyed3

def checkMp3(path):
    if path.lower().endswith('.mp3'):
        return True
    else:
        return False

def main():
    print("Hello World!")

if __name__ == "__main__":
    sys.exit(int(main() or 0))