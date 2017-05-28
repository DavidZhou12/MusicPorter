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

# Prints editable EasyID3 tags
def print_editable_list():
    print('\n'.join(EasyID3.valid_keys.keys()))

def is_mp3(file_name):
    if file_name.lower().endswith('.mp3'):
        return True
    else:
        return False

def get_current_directory_mp3():
    mp3_files = [file for file in os.listdir() if is_mp3(file)]
    return mp3_files

# Ensures every mp3 file in the list has an ID3 tag with: title, album, artist
# Returns a sorted list of every mp3 file
def get_sorted_list(mp3_files):
    sorted_list = []
    for mp3_file_path in mp3_files:
        try:                                    # Test if the file has an ID3 tag
            audio_file = EasyID3(mp3_file_path)

            #Check if the three tags are in the ID3 file
            modified_flag = False
            if "title" not in audio_file or "album" not in audio_file or "artist" not in audio_file:
                modified_flag = True
            if "title" not in audio_file:
                audio_file["title"] = [os.path.splitext(mp3_file_path)[0]]
            if "album" not in audio_file:
                audio_file["album"] = [u"Unknown Album"]
            if "artist" not in audio_file:
                audio_file["artist"] = [u"Unknown Artist"]
            if modified_flag == True:
                audio_file.save(mp3_file_path, v1=2, v2_version = 3)

        except mutagen.id3.ID3NoHeaderError:    # If no ID3 tag present, create one
            audio_file = EasyID3()
            audio_file["title"] = [os.path.splitext(mp3_file_path)[0]]
            audio_file["album"] = [u"Unknown Album"]
            audio_file["artist"] = [u"Unknown Artist"]
            audio_file.save(mp3_file_path, v1=2, v2_version = 3)
        sorted_list.append((mp3_file_path, audio_file["title"][0], audio_file["album"][0], audio_file["artist"][0]))
    
    # Multi-level sorting
    sorted_list = sorted(sorted_list, key=itemgetter(2, 3, 1, 0))
        
    # Expect every item to have an ID3 tag at this point
    # Add track number to mp3 files based on the sorted list
    sorted_list_with_tracknumber = []
    track_number = 1
    for item in sorted_list:
        audio_file = EasyID3(item[0])
        audio_file["tracknumber"] = [str(track_number)]
        audio_file.save(item[0], v1=2, v2_version = 3)
        sorted_list_with_tracknumber.append((item[0], item[1], item[2], item[3], audio_file["tracknumber"][0]))
        track_number += 1

    return sorted_list_with_tracknumber

# Expects all items in the list to have an ID3 tag with atleast: title, album, and artist
def write_output(sorted_list):

    # encoding="utf-8" accounts for text written in other languages
    with io.open("Music Menu.txt", "w", encoding="utf-8") as output:

        # Get padding size for neat formating
        col_width1 = 1
        col_width2 = 1
        col_width4 = 1
        for item in sorted_list:
            if len(item[1]) > col_width1:
                col_width1 = len(item[1])
            if len(item[2]) > col_width2:
                col_width2 = len(item[2])
            if len(item[4]) > col_width4:
                col_width4 = len(item[4])
        # Padding
        col_width1 += -94    # For lengthy titles
        col_width2 += -42
        col_width4 += 2

        for item in sorted_list:
            output.write(item[4].ljust(col_width4) + ' ' + item[1].ljust(col_width1, '.') + ' ' + ''.ljust(1, '\t') + ' ' + item[2].ljust(col_width2, '.') + ' ' + ''.ljust(1, '\t') + ' ' + item[3] + '\n')

# Converts user input raw_path into unicode_path
# Transfer files one by one
def transfer_files(sorted_list, raw_path):
    for item in sorted_list:
        unicode_path = raw_path.replace('\\', "\\\\")
        print("Copying " + item[0] + "...")
        copy2(item[0], unicode_path)

def main():
    # Prepare for transfer
    print("Acquiring MP3 files within the directory...\n")
    mp3_files = get_current_directory_mp3()
    print("Sorting MP3 files within the directory...\n")
    sorted_mp3_files = get_sorted_list(mp3_files)
    print("Creating list of sorted MP3 files within the directory: \"Music Menu\"\n")
    write_output(sorted_mp3_files)
    
    # Transfer mp3 files to a specified directory
    path = input("Enter the path to transfer the music to: ")
    print("Transfering music to: ", path)
    transfer_files(sorted_mp3_files, path)

    print("-- TRANSFER COMPLETE --\n")

if __name__ == "__main__":
    sys.exit(int(main() or 0))