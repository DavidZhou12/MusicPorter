import eyed3
import os, songdetails, sys

def isMp3(fileName):
    if fileName.lower().endswith('.mp3'):
        return True
    else:
        return False

def GetCurrentDirectoryMp3List():
    mp3Files = [file for file in os.listdir() if isMp3(file)]
    return mp3Files

def sortMp3Files(mp3Files):
    

def main():
    mp3Files = GetCurrentDirectoryMp3List()
    print(*mp3Files, sep='\n')
    audiofile = eyed3.load(mp3Files[0])
    print(audiofile.tag.title)

if __name__ == "__main__":
    sys.exit(int(main() or 0))