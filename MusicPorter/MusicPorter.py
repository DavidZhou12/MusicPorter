import mpeg1audio
import os, songdetails, sys

def isMp3(fileName):
    if fileName.lower().endswith('.mp3'):
        return True
    else:
        return False

def GetCurrentDirectoryMp3List():
    mp3Files = [file for file in os.listdir() if isMp3(file)]
    return mp3Files

def main():
    mp3Files = GetCurrentDirectoryMp3List()
    print(*mp3Files, sep='\n')
    print(mp3Files[0])
    '''
    song = songdetails.scan(mp3Files[0])
    
    if song is not None:
        print(song.artist)
        '''

if __name__ == "__main__":
    sys.exit(int(main() or 0))