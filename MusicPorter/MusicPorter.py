import mutagen
from mutagen import *
import os, sys

def isMp3(fileName):
    if fileName.lower().endswith('.mp3'):
        return True
    else:
        return False

def GetCurrentDirectoryMp3List():
    mp3Files = [file for file in os.listdir() if isMp3(file)]
    return mp3Files

def sortMp3Files(mp3Files):
    return True

def main():
    mp3Files = GetCurrentDirectoryMp3List()
    print(*mp3Files, sep='\n')
    try:
        audioFile = EasyID3(mp3Files[1])
    except mutagen.id3.ID3NoHeaderError:
        audioFile = mutagen.File(mp3Files[1], EasyID3=True)
        audioFile.add_tags()



    #audioFile = EasyID3(mp3Files[1])
    #print(audioFile['title'])
            
if __name__ == "__main__":
    sys.exit(int(main() or 0))