#Python Modules
from pathlib import Path
import os
import re # for regex
import threading # for multithreading

#Other Modules
from pytube import YouTube
from pytube.cli import on_progress  # for progress bar in terminal
import ffmpeg
import PySimpleGUI as sg

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

    ffmpeg.concat(input_video, input_audio, v=1, a=1).output(outputfile).run(overwrite_output=True)

    print("\nCombining complete.")
    print("---------------------------------------------------------")
    print("Deleting duplicate audio and video files...")
    os.remove(audioPath) #deletes both audio and video files in their respective folders
    os.remove(videoPath) 
    print("Deletion complete.")
    print("---------------------------------------------------------")
    print("Preparing Next Link...\n")

def multithreadDownload(audioSP, videoSP, combineSP, ytLinks):   
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

    threads = [] #creates a list of threads
    for link in ytLinks:
        link = str(link) #converts the list of links into a string for the function below
        link = link[2:-2] #removes first two and last two characters from the string, {} and ''
        t = threading.Thread(target=downloadBoth, args=(link,)) #creates a thread for each link

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

    # link = input("Enter your link: ")
    multithreadDownload(audioSP, videoSP, combineSP, ytLinks)