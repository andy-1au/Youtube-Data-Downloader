#Python Modules
from pathlib import Path
import os
import re # for regex
import threading # for multithreading
import time
from datetime import timedelta 

#Other Modules
from pytube import YouTube
from pytube.cli import on_progress  # for progress bar in terminal
import ffmpeg
import PySimpleGUI as sg

#Next thing to do: change names of videos to the their respective IDs

def parseID(file):
    default_link = "https://www.youtube.com/watch?v="
    with open(file, 'r') as f: # 'with' closes the file for you
        id_list = [line.rstrip() for line in f] #removes the newline character from the end of each line
        link_list = [{default_link + id} for id in id_list] # creates a list of links from the list of ids
    # print(f"IDs: {id_list}") #DEBUG
    # print(f"Links: {link_list}") #DEBUG
    return link_list 

def combineFiles(audioPath, videoPath, combineSP, fileName):
    
    print("Combining audio and video files...")
    print("---------------------------------------------------------")
    print(f"File Name: {fileName}")
    print("---------------------------------------------------------")
    outputfile = os.path.join(combineSP, f"{fileName}.mp4")
    print("Output File: " + str(outputfile))
    
    # print(f"\nAudio File: {audiofile}") #DEBUG
    # print (f"Video File: {videofile}") #DEBUG
    # print(f"Output File: {outputfile}") #DEBUG

    input_video = ffmpeg.input(videoPath)
    input_audio = ffmpeg.input(audioPath)
    print("---------------------------------------------------------")
    print("Input Video: " + str(input_video))
    print("\nInput Audio: " + str(input_audio))
    print("---------------------------------------------------------")

    ffmpeg.concat(input_video, input_audio, v=1, a=1).output(outputfile, vcodec="h264_nvenc").run(overwrite_output=True)

    print("\nCombining complete.")
    print("---------------------------------------------------------")
    print("Deleting duplicate audio and video files...")
    os.remove(audioPath) #deletes both audio and video files in their respective folders
    os.remove(videoPath) 
    print("Deletion complete.")
    print("---------------------------------------------------------")
    print("Preparing Next Link...\n")

def multiThreadDownload(audioSP, videoSP, combineSP, ytLinks, fileNameFormat):   
    def downloadBoth(link):
        try:
            print(f"Downloading From: {link}") #DEBUG
            print("---------------------------------------------------------")

            print("\nDownloading Video File...")
            videoObject = YouTube(link, on_progress_callback=on_progress)
            audioObject = YouTube(link, on_progress_callback=on_progress)

            videoObject = videoObject.streams.filter(adaptive=True, file_extension='mp4').order_by('resolution').desc().first()

            print(f"Video Object: {videoObject}") #DEBUG
            videoName = videoObject.title
        
            videoName = re.sub(r'[.#%&{}\\<>*?/\$!\'\":@+`|=]', '', videoName) #delete special characters from video name to avoid errors
            print(f"Video Name: {videoName}") #DEBUG
            # vtag = videoObject.itag #DEBUG
            # print(str(vtag) + " is the itag of the video stream.") #DEBUG
            videoObject.download(videoSP)
            print("Video Download Complete.")
            print("---------------------------------------------------------")

            print("\nDownloading Audio File..")
            audioObject = audioObject.streams.filter(only_audio=True).first()

            print(f"Audio Object: {audioObject}") #DEBUG
            audioName = audioObject.title

            audioName = re.sub(r'[.#%&{}\\<>*?/\$!\'\":@+`|=]', '', audioName)
            print(f"Audio Name: {audioName}") #DEBUG
            # atag = audioObject.itag #DEBUG
            # print(str(atag) + " is the itag of the audio stream.") #DEBUG
            audioObject.download(audioSP)
            print("Audio Download Complete.")
            print("\nBoth Download complete.")
            print("---------------------------------------------------------")

            newAudioPath = Path(audioSP, f"{audioName}.mp4")
            newVideoPath = Path(videoSP, f"{videoName}.mp4")

            combineFiles(newAudioPath, newVideoPath, combineSP, videoName) 

        except Exception as e:
            print('Error: Unable to download audio and video files:', e)
            return None
            exit()

    threads = [] #creates a list of threads
    for link in ytLinks:
        link = str(link) #converts the list of links into a string for the function below
        link = link[2:-2] #removes first two and last two characters from the string, {} and ''
        #creates a thread for each link, and passes the link as an argument
        #comma is needed after the argument, even if there is only one argument because it is a tuple
        thread = threading.Thread(target=downloadBoth, args=(link,)) 
        threads.append(thread) #adds the thread to the list of threads
        thread.start() #starts the thread
    
    for thread in threads:
        thread.join() #waits for all threads to finish before continuing, ensures that all downloads and combinations are complete before the program ends

def singleThreadDownload(audioSP, videoSP, combineSP, ytLinks, fileNameFormat):
    for link in ytLinks: 
        try:
            link = str(link) #converts the list of links into a string for the function below
            link = link[2:-2] #removes first two and last two characters from the string, {} and ''
            print(f"Downloading From: {link}") #DEBUG
            print("---------------------------------------------------------")

            print("\nDownloading Video File...")
            videoObject = YouTube(link, on_progress_callback=on_progress)
            audioObject = YouTube(link, on_progress_callback=on_progress)

            videoObject = videoObject.streams.filter(adaptive=True, file_extension='mp4').order_by('resolution').desc().first()

            print(f"Video Object: {videoObject}") #DEBUG
            videoName = videoObject.title
        
            videoName = re.sub(r'[.#%&{}\\<>*?/\$!\'\":@+`|=]', '', videoName) #delete special characters from video name to avoid errors
            print(f"Video Name: {videoName}") #DEBUG
            # vtag = videoObject.itag #DEBUG
            # print(str(vtag) + " is the itag of the video stream.") #DEBUG
            videoObject.download(videoSP)
            print("Video Download Complete.")
            print("---------------------------------------------------------")

            print("\nDownloading Audio File..")
            audioObject = audioObject.streams.filter(only_audio=True).first()

            print(f"Audio Object: {audioObject}") #DEBUG
            audioName = audioObject.title

            audioName = re.sub(r'[.#%&{}\\<>*?/\$!\'\":@+`|=]', '', audioName)
            print(f"Audio Name: {audioName}") #DEBUG
            # atag = audioObject.itag #DEBUG
            # print(str(atag) + " is the itag of the audio stream.") #DEBUG
            audioObject.download(audioSP)
            print("Audio Download Complete.")
            print("\nBoth Download complete.")
            print("---------------------------------------------------------")

            newAudioPath = Path(audioSP, f"{audioName}.mp4")
            newVideoPath = Path(videoSP, f"{videoName}.mp4")

            combineFiles(newAudioPath, newVideoPath, combineSP, videoName) 

        except Exception as e:
            print('Error: Unable to download audio and video files:', e)
            return None
        
def menu():
    print("Welcome to the YouTube Downloader!")
    print("This program will download the audio and video files from a YouTube video, and combine them into a single file.")
    print("--------------------------------------------")
    print("Please select an option for naming the downloaded files below:")
    print("[1] By Original Name\n[2] By Video ID")

    while True:
        fileNameFormat = input("Enter your selection: ")
        if fileNameFormat == "1":
            print("Your files will be named by their original name.")
            break
        elif fileNameFormat == "2":
            print("Your files will be named by their video ID.")
            break
        else:
            print("Invalid input. Please try again.")
            continue
    
    print("--------------------------------------------")
    print("Please select an option for downloading the files below:")
    print("[1] Single Thread\n[2] Multi Thread")

    while True:
        downloadFormat = input("Enter your selection: ")
        if downloadFormat == "1":
            print("Your files will be downloaded using a single thread.")
            break
        elif downloadFormat == "2":
            print("Your files will be downloaded using multiple threads.")
            break
        else:
            print("Invalid input. Please try again.")
            continue
    return fileNameFormat, downloadFormat

# Main Function 
if __name__ == '__main__':

    #NOTE: When using a new path, make sure to replace the backslash with forward slash. Relative pathing also works, and might be the best way to do it when testing the scripts
    # audioSP = Path("Insert Path Here")
    # videoSP = Path("Insert Path Here")
    # combineSP = Path("Insert Path Here")
    audioSP = Path("Audios Folder")
    videoSP = Path("Videos Folder")
    combineSP = Path("Combine Folder")
    
    ytLinks = parseID("video_ids.txt")

    start = time.time()
    #--------------------------------------------
    fileNameFormat, downloadFormat = menu()
    if downloadFormat == "1":
        singleThreadDownload(audioSP, videoSP, combineSP, ytLinks, fileNameFormat)
    elif downloadFormat == "2":
        multiThreadDownload(audioSP, videoSP, combineSP, ytLinks, fileNameFormat)
    # singleThreadDownload(audioSP, videoSP, combineSP, ytLinks)
    # multiThreadDownload(audioSP, videoSP, combineSP, ytLinks)

    #--------------------------------------------
    end = time.time()

    total_time = end - start
    formatted_time = str(timedelta(seconds=total_time))
    print(f"\nTotal Time: {formatted_time}")
