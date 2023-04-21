#Python Modules
from pathlib import Path
import os # removals and paths
import sys # system functions
import re # regex
import time # time functions 
from datetime import timedelta # time formatting 
from concurrent.futures import ThreadPoolExecutor

# Third Party Modules
import yt_dlp # YouTube Downloader
import tqdm # progress bar

 
def download(ydl_opts, idList, fileNameFormat):
    if fileNameFormat == "1":
        ydl_opts['outtmpl'] = str(combineSP / '%(title)s.%(ext)s')
    elif fileNameFormat == "2":
        ydl_opts['outtmpl'] = str(combineSP / '%(id)s.%(ext)s')

    for video_id in idList:
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_id])
        except yt_dlp.utils.DownloadError:
            print(f"Video {video_id} not downloaded. Skipping...")
            continue

def parseID(file):
    with open(file, 'r') as f: # 'with' closes the file for you
        idList = [line.rstrip() for line in f] #removes the newline character from the end of each line
    # print(f"IDs: {idList}") #DEBUG
    return idList

def menu(directory):
    print("\nWelcome to the YouTube Downloader!")
    print("This program will download the audio and video files from a YouTube link and combine them into a single file!")
    print("--------------------------------------------")
    
    files = [f for f in os.listdir(directory) if f.endswith('.txt')] # Get a list of all text files in the directory

    print(f"Please select a file from the following list:") #
    while True:
        try: 
            for i, file in enumerate(files): #enumerate() returns the index and the value of the list
                print(f"[{i+1}] {file}") #  Display the list of files to the user, +1 for the user's convenience
            choice = input("Enter a number (or Q to quit): ")
            if choice.lower() == "q":
                exit()
            elif int(choice) in range(1, len(files)+1): # Check if the user's input is a valid number
                fileName = files[int(choice)-1] # Get the file name from the list, -1 because the list starts at 0
                print(f"You selected {fileName}.")
                break
            else:
                print("Invalid input. Please try again.")
                continue
        except ValueError:
            print("Invalid input. Please try again.")
            continue
    
    print("Please select an option for naming the downloaded files below:")
    print("[1] By Original Name\n[2] By Video ID\n")

    while True:
        fileNameFormat = input("Enter your selection (or Q to quit): ")
        if fileNameFormat.lower() == "q":
            exit()
        elif fileNameFormat == "1":
            print("\nYour files will be named by their original name.")
            break
        elif fileNameFormat == "2":
            print("\nYour files will be named by their video ID.")
            break
        else:
            print("Invalid input. Please try again.")
            continue
    return fileNameFormat, fileName

if __name__ == '__main__':
    audioSP = Path("Audios Folder")
    videoSP = Path("Videos Folder")
    combineSP = Path("Combine Folder")
    idSP = Path("ID Folder")

    fileNameFormat, fileName = menu(idSP) #calls menu function

    idList = parseID("ID Folder/" + fileName)  

    print("List of ids:" + str(idList))

    ydl_opts = {
        # Download Options
        'format': 'best',
        'outtmpl': str(combineSP / '%(id)s.mp4'),

        # Post-processing Options
        'merge_output_format': 'mp4',

        # Hardware Acceleration Options
        'video-codec': 'nvenc',
        'gpu': True,

        # Performance Options
        'n_threads': 8, # not sure if this is working

        # Conflict Resolution Options
        'nooverwrites': False, # Overwrite files if they already exist (default: True)

        # External Downloader Options
        'external_downloader': 'ffmpeg',
    }

    start = time.time()
    #----------------------------------------------
    download(ydl_opts, idList, fileNameFormat)
    #----------------------------------------------
    end = time.time()

    totalTime = end - start
    formattedTime = str(timedelta(seconds=totalTime))

    print("\nAll files have been downloaded and combined!")
    print(f"\nTotal Time: {formattedTime}")

    #"C:\Program Files\ffmpeg\bin\ffmpeg.exe"