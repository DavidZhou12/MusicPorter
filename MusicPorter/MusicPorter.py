import mutagen
from mutagen.easyid3 import EasyID3
import io, os, sys

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
        audioFile = EasyID3(mp3Files[0])
    except mutagen.id3.ID3NoHeaderError:
        audioFile = mutagen.File(mp3Files[0])
        audioFile.add_tags()
    print(audioFile['title'])

    with io.open("Output.txt", "w", encoding="utf-8") as file:
        #file.write(" ".join(str(x) for x in audioFile['title']))
        file.write(audioFile['title'][0])



    #audioFile = EasyID3(mp3Files[1])
    #print(audioFile['title'])
            
if __name__ == "__main__":
    sys.exit(int(main() or 0))