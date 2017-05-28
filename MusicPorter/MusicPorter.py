import mutagen
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, TIT2
import io, os, sys
from operator import itemgetter, attrgetter

# Items in the mp3List are in tuples with the following order:
# (mp3FilePath, Title, Album, Artist, Track Number)

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

# Ensures every mp3 file in the list has an ID3 tag with: title, album, artist
# Returns a sorted list of every mp3 file
def getSortedList(mp3Files):
    sortedList = []
    for mp3FilePath in mp3Files:
        try:                                    # Test if the file has an ID3 tag
            audioFile = EasyID3(mp3FilePath)

            #Check if the three tags are in the ID3 file
            modified_flag = False
            if "title" not in audioFile or "album" not in audioFile or "artist" not in audioFile:
                modified_flag = True
            if "title" not in audioFile:
                audioFile["title"] = [os.path.splitext(mp3FilePath)[0]]
            if "album" not in audioFile:
                audioFile["album"] = ["Unknown Album"]
            if "artist" not in audioFile:
                audioFile["artist"] = ["Unknown Artist"]
            if modified_flag == True:
                audioFile.save(mp3FilePath, v1=2, v2_version = 3)

        except mutagen.id3.ID3NoHeaderError:    # If no ID3 tag present, create one
            audioFile = EasyID3()
            audioFile["title"] = [os.path.splitext(mp3FilePath)[0]]
            audioFile["album"] = ["Unknown Album"]
            audioFile["artist"] = ["Unknown Artist"]
            audioFile.save(mp3FilePath, v1=2, v2_version = 3)

        sortedList.append((mp3FilePath, audioFile['title'][0], audioFile['album'][0], audioFile['artist'][0]))
        sortedList = sorted(sortedList, key=itemgetter(2, 3, 1, 0))
        
        # Except every item to have an ID3 tag at this point

    return sortedList

# Expects all items in the list to have an ID3 tag with atleast: title, album, and artist
def writeOutput(sortedList):

    # encoding="utf-8" accounts for text written in other languages
    with io.open("Output.txt", "w", encoding="utf-8") as output:
        for mp3File in sortedList:
            output.write(audioFile['title'][0] + ' ' + audioFile['album'][0] + ' ' + audioFile['artist'][0] + '\n')

def main():
    mp3Files = GetCurrentDirectoryMp3List()
    #print(*mp3Files, sep='\n')
    sortedMp3Files = getSortedList(mp3Files)
    print(*sortedMp3Files, sep='\n');
    #writeOutput(mp3Files)
    #print(EasyID3(mp3Files[0]))

if __name__ == "__main__":
    sys.exit(int(main() or 0))