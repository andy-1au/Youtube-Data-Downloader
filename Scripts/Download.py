#Python Modules
from pathlib import Path
import os # removals and paths
import re # regex

import threading # multithreading
from concurrent.futures import ThreadPoolExecutor

import time # time functions 
from datetime import timedelta # time formatting 

#Other Modules
from pytube import YouTube
from pytube.cli import on_progress  # for progress bar in terminal
import ffmpeg

def parseID(file):
    with open(file, 'r') as f: # 'with' closes the file for you
        idList = [line.rstrip() for line in f] #removes the newline character from the end of each line
    # print(f"IDs: {idList}") #DEBUG
    return idList

def combineFiles(audioPath, videoPath, combineSP, fileName):
    
    print("Combining audio and video files...")
    print("---------------------------------------------------------")
    print(f"File Name: {fileName}")
    print("---------------------------------------------------------")
    outputfile = os.path.join(combineSP, f"{fileName}")
    print("Output File: " + str(outputfile))
    
    # print(f"\nAudio File: {audiofile}") #DEBUG
    # print (f"Video File: {videofile}") #DEBUG
    # print(f"Output File: {outputfile}") #DEBUG

    inputVideo = ffmpeg.input(videoPath)
    inputAudio = ffmpeg.input(audioPath)
    print("---------------------------------------------------------")
    print("Input Video: " + str(inputVideo))
    print("\nInput Audio: " + str(inputAudio))
    print("---------------------------------------------------------")

    # vcodec="h264_nvenc" #for nvidia gpu, add this as a parameter to the output function
    if selectedCodec == "1":
        ffmpeg.concat(inputVideo, inputAudio, v=1, a=1).output(outputfile).run(overwrite_output=True)
    elif selectedCodec == "2":
        ffmpeg.concat(inputVideo, inputAudio, v=1, a=1).output(outputfile, vcodec="h264_nvenc").run(overwrite_output=True)
    elif selectedCodec == "3": 
        ffmpeg.concat(inputVideo, inputAudio, v=1, a=1).output(outputfile, vcodec="hevc_nvenc").run(overwrite_output=True) 

    print("\nCombining complete.")
    print("---------------------------------------------------------")
    print("Deleting duplicate audio and video files...")

    # os.remove(audioPath) #deletes both audio and video files in their respective folders
    os.remove(videoPath) 
    os.remove(audioPath)

    print("Deletion complete.")
    print("---------------------------------------------------------")
    print("Preparing Next Link...\n")

def downloadBoth(link, id):
    try:
        print(f"Downloading From: {link}") #DEBUG
        print("---------------------------------------------------------")

        print("\nDownloading Video File...")
        videoObject = YouTube(link, on_progress_callback=on_progress)
        audioObject = YouTube(link, on_progress_callback=on_progress)

        videoObject = videoObject.streams.filter(adaptive=True, file_extension='mp4').order_by('resolution').desc().first()

        print(f"Video Object: {videoObject}") #DEBUG
        # vtag = videoObject.itag #vtag is the itag of the video stream
        # print(str(vtag) + " is the itag of the video stream.") #DEBUG

        if fileNameFormat == "2":
            videoName = id + ".mp4"
            print(f"Video Name: {videoName}") #DEBUG
            videoObject.download(videoSP, filename=videoName) 
        else:
            videoName = videoObject.title
            videoName = re.sub(r'[.#%&{}\\<>*?/\$!\'\":@+`|=]', '', videoName) #delete special characters from video name to avoid errors
            videoName = videoName + ".mp4"
            print(f"Video Name: {videoName}") #DEBUG
            videoObject.download(videoSP, filename=videoName)

        print("Video Download Complete.")
        print("---------------------------------------------------------")

        print("\nDownloading Audio File..")
        audioObject = audioObject.streams.filter(only_audio=True).first()

        print(f"Audio Object: {audioObject}") #DEBUG
        # atag = audioObject.itag #atag is the itag of the audio stream
        # print(str(atag) + " is the itag of the audio stream.") #DEBUG

        if fileNameFormat == "2":
            audioName = id + ".mp4"
            print(f"Audio Name: {audioName}") #DEBUG
            audioObject.download(audioSP, filename=audioName)
        else:
            audioName = audioObject.title
            audioName = re.sub(r'[.#%&{}\\<>*?/\$!\'\":@+`|=]', '', audioName)
            audioName = audioName + ".mp4"
            print(f"Audio Name: {audioName}") #DEBUG
            audioObject.download(audioSP, filename=audioName)

        print("Audio Download Complete.")
        print("\nBoth Download complete.")
        print("---------------------------------------------------------")
        newAudioPath = Path(audioSP, f"{audioName}")
        newVideoPath = Path(videoSP, f"{videoName}")

        combineFiles(newAudioPath, newVideoPath, combineSP, videoName) 

    except Exception as e:
        print('Error: Unable to download audio and video files:', e)
        return None

def multiThreadDownload(idList):  
    maxThreads = int(numThreads) #set number of threads here, 3 seems to be working fine with rtx 3060

    with ThreadPoolExecutor(max_workers=maxThreads) as executor: #thread limiting function
        defaultLink = "https://www.youtube.com/watch?v="
        for id in idList:
            link = defaultLink + id
            executor.submit(downloadBoth, link, id) #submit function with args to be executed in a separate thread`

def singleThreadDownload(idList):
    defaultLink = "https://www.youtube.com/watch?v="

    for id in idList: 
        link = defaultLink + id
        downloadBoth(link, id)
        
def menu():
    print("\nWelcome to the YouTube Downloader!")
    print("This program will download the audio and video files from a YouTube link and combine them into a single file!")
    print("--------------------------------------------")
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
    
    print("--------------------------------------------")
    print("Please select an option for downloading the files below:")
    print("[1] Single-threading\n[2] Multi-threading\n")

    while True:
        downloadFormat = input("Enter your selection (or Q to quit): ")
        if downloadFormat.lower() == "q":
            exit()
        elif downloadFormat == "1":
            print("\nYour files will be downloaded using a single thread.")
            break
        elif downloadFormat == "2":
            while True:
                numThreads = input("Enter the number of threads you want to use (2-4) (or Q to quit): ")
                if numThreads.lower() == "q":
                    exit()
                if numThreads.isdigit() and int(numThreads) in range(2, 5):
                    print(f"\nYour files will be downloaded using {numThreads} threads.")
                    break
                else:
                    print("Invalid input. Please enter a number between 2 and 4.")
            break
        else:
            print("Invalid input. Please try again.")
            continue

    print("--------------------------------------------")
    print("Please select an video codec for encoding:")
    print("[1] Default Codec (CPU)\n[2] NVIDIA Default Codec (h264_nvenc)\n[3] NVIDIA Experimental Codec (hevc_nvenc)\n")

    while True: 
        selectedCodec = input("Enter your selection (or Q to quit): ")
        if selectedCodec.lower() == "q":
            exit()
        elif selectedCodec == "1":
            print("The default codec will be used for encoding.")
            break
        elif selectedCodec == "2":
            print("The NVIDIA default codec (h264_nvenc) will be used for encoding.")
            break
        elif selectedCodec == "3":
            print("The NVIDIA experimental codec (hevc_nvenc) will be used for encoding.")
            break
        else:
            print("Invalid input. Please try again.")
            continue

    return fileNameFormat, downloadFormat, selectedCodec, numThreads

if __name__ == '__main__':
    #NOTE: When using a new path, make sure to replace the backslash with forward slash. Relative pathing also works, and might be the best way to do it when testing the scripts
    # audioSP = Path("Insert Path Here")
    # videoSP = Path("Insert Path Here")
    # combineSP = Path("Insert Path Here")
    audioSP = Path("Audios Folder")
    videoSP = Path("Videos Folder")
    combineSP = Path("Combine Folder")
    
    idList = parseID("3min.txt") #input list of ids   

    fileNameFormat, downloadFormat, selectedCodec, numThreads = menu() #calls menu function

    #--------------------------------------------
    start = time.time()
    if downloadFormat == "1":
        singleThreadDownload(idList)
    elif downloadFormat == "2":
        multiThreadDownload(idList)
    end = time.time()
    #--------------------------------------------

    totalTime = end - start
    formattedTime = str(timedelta(seconds=totalTime))
    print(f"\nTotal Time: {formattedTime}")
