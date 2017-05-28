import mutagen
from mutagen.easyid3 import EasyID3
import io, os, sys
from operator import itemgetter, attrgetter
from shutil import copy2
from codecs import decode

#
# This program analyzes mp3 files within the current directory
# and generates ID3 tags for files that are missing an ID3 for: title, album and artist
# A sorted list will be generated with multi-level sorting.
# Sorting order: Album -> Artist -> Title
# Each track will be assigned a tracking number based on it's index in the sorted list.
# The program then transfers every mp3 to the user's input path.
# The files will be transfered one-by-one based on the track number.
# This is particularly useful for media player devices that plays audio tracks based
# on time of insertion into the device.
# 
# Items in the mp3List are in tuples with the following order:
# (mp3FilePath, Title, Album, Artist, Track Number)
#

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
                audioFile["album"] = [u"Unknown Album"]
            if "artist" not in audioFile:
                audioFile["artist"] = [u"Unknown Artist"]
            if modified_flag == True:
                audioFile.save(mp3FilePath, v1=2, v2_version = 3)

        except mutagen.id3.ID3NoHeaderError:    # If no ID3 tag present, create one
            audioFile = EasyID3()
            audioFile["title"] = [os.path.splitext(mp3FilePath)[0]]
            audioFile["album"] = [u"Unknown Album"]
            audioFile["artist"] = [u"Unknown Artist"]
            audioFile.save(mp3FilePath, v1=2, v2_version = 3)
        sortedList.append((mp3FilePath, audioFile["title"][0], audioFile["album"][0], audioFile["artist"][0]))
    
    # Multi-level sorting
    sortedList = sorted(sortedList, key=itemgetter(2, 3, 1, 0))
        
    # Expect every item to have an ID3 tag at this point
    # Add track number to mp3 files based on the sorted list
    sortedListWithTrackNumbers = []
    trackNumber = 1
    for item in sortedList:
        audioFile = EasyID3(item[0])
        audioFile["tracknumber"] = [str(trackNumber)]
        audioFile.save(item[0], v1=2, v2_version = 3)
        sortedListWithTrackNumbers.append((item[0], item[1], item[2], item[3], audioFile["tracknumber"][0]))
        trackNumber += 1

    return sortedListWithTrackNumbers

# Expects all items in the list to have an ID3 tag with atleast: title, album, and artist
def writeOutput(sortedList):

    # encoding="utf-8" accounts for text written in other languages
    with io.open("Music Menu.txt", "w", encoding="utf-8") as output:

        # Get padding size for neat formating
        colWidth1 = 1
        colWidth2 = 1
        colWidth4 = 1
        for item in sortedList:
            if len(item[1]) > colWidth1:
                colWidth1 = len(item[1])
            if len(item[2]) > colWidth2:
                colWidth2 = len(item[2])
            if len(item[4]) > colWidth4:
                colWidth4 = len(item[4])
        # Padding
        colWidth1 += -94    # For lengthy titles
        colWidth2 += -42
        colWidth4 += 2

        for item in sortedList:
            output.write(item[4].ljust(colWidth4) + ' ' + item[1].ljust(colWidth1, '.') + ' ' + ''.ljust(1, '\t') + ' ' + item[2].ljust(colWidth2, '.') + ' ' + ''.ljust(1, '\t') + ' ' + item[3] + '\n')

def transferFiles(sortedList, path):
    for item in sortedList:
        properPath = path.replace('\\', "\\\\")
        print("Copying " + item[0] + "...")
        copy2(item[0], properPath)

def main():
    # Prepare for transfer
    print("Acquiring MP3 files within the directory...\n")
    mp3Files = GetCurrentDirectoryMp3List()
    print("Sorting MP3 files within the directory...\n")
    sortedMp3Files = getSortedList(mp3Files)
    print("Creating list of sorted MP3 files within the directory: \"Music Menu\"\n")
    writeOutput(sortedMp3Files)
    
    # Transfer mp3 files to a specified directory
    path = input("Enter the path to transfer the music to: ")
    print("Transfering music to: ", path)
    transferFiles(sortedMp3Files, path)

    print("-- TRANSFER COMPLETE --\n")

if __name__ == "__main__":
    sys.exit(int(main() or 0))