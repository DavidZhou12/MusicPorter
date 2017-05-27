import mutagen
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, TIT2
import io, os, sys

def printEditableList():
    print('\n'.join(EasyID3.valid_keys.keys()))

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

def writeOutput(mp3Files):
    with io.open("Output.txt", "w", encoding="utf-8") as output:
        for mp3File in mp3Files:
            try:                                    # Test if file has an ID3 tag
                audioFile = EasyID3(mp3File)
            except mutagen.id3.ID3NoHeaderError:    # if it doesn't have an ID3 tag, create an ID3 tag for it
                audioFile = EasyID3()
                audioFile["title"] = [os.path.splitext(mp3File)[0]]
                audioFile["album"] = ["Unknown Album"]
                audioFile['artist'] = ["Unknown Artist"]
                audioFile.save(mp3File, v1=2, v2_version = 3)
            output.write(audioFile['title'][0] + ' ' + audioFile['album'][0] + ' ' + audioFile['artist'][0] + '\n')

def main():
    mp3Files = GetCurrentDirectoryMp3List()
    print(*mp3Files, sep='\n')
    writeOutput(mp3Files)
    #print(EasyID3(mp3Files[0]))

if __name__ == "__main__":
    sys.exit(int(main() or 0))