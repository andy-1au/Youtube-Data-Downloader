#Python Modules
from pathlib import Path
import os
import re # for regex

#Other Modules
from pytube import YouTube
from pytube.cli import on_progress  # for progress bar in terminal
import ffmpeg
import PySimpleGUI as sg

def combineFiles(audioPath, videoPath, combineSP, fileName):
    
    print("\nCombining audio and video files...")
    print("---------------------------------------------------------")
    print(f"\nfileName: {fileName}")
    print("---------------------------------------------------------")
    outputfile = os.path.join(combineSP, f"{fileName}.mp4")
    print("Output File: " + str(outputfile))
    
    # print(f"\nAudio File: {audiofile}") #debug
    # print (f"Video File: {videofile}") #debug
    # print(f"Output File: {outputfile}") #debug

    input_video = ffmpeg.input(videoPath)
    input_audio = ffmpeg.input(audioPath)
    print("---------------------------------------------------------")
    print("Input Video: " + str(input_video))
    print("Input Audio: " + str(input_audio))
    print("---------------------------------------------------------")

    ffmpeg.concat(input_video, input_audio, v=1, a=1).output(outputfile).run(overwrite_output=True)

    print("\nCombining complete.")

def downloadBoth(link, audioSP, videoSP):
    videoObject = YouTube(link, on_progress_callback=on_progress)
    audioObject = YouTube(link, on_progress_callback=on_progress)
    try:
        print("\nDownloading Video File...")

        videoObject = videoObject.streams.filter(adaptive=True, file_extension='mp4').order_by('resolution').desc().first()
        print(videoObject)  # debug
        videoName = videoObject.title
        #delete special characters from video name to avoid errors
        videoName = re.sub(r'[.#%&{}\\<>*?/\$!\'\":@+`|=]', '', videoName)
        print(videoName) #debug
        # vtag = videoObject.itag #debug
        # print(str(vtag) + " is the itag of the video stream.") #debug
        videoObject.download(videoSP)

        print("\nDownloading Audio File..")
        audioObject = audioObject.streams.filter(only_audio=True).first()
        print(audioObject)  # debug
        audioName = audioObject.title
        audioName = re.sub(r'[.#%&{}\\<>*?/\$!\'\":@+`|=]', '', audioName)
        print(audioName) #debug
        # atag = audioObject.itag #debug
        # print(str(atag) + " is the itag of the audio stream.") #debug
        audioObject.download(audioSP)

        print("\nDownload complete.")

        newAudioPath = Path(audioSP, f"{audioName}.mp4")
        newVideoPath = Path(videoSP, f"{videoName}.mp4")

        return newAudioPath, newVideoPath, videoName

    except:
        print('Error: Unable to download video.')

# Main Function 
if __name__ == '__main__':
    audioSP = Path("C:/Users/andyr/OneDrive - Lehigh University/DESKTOP/Projects/Workstudy/Youtube-Downloader-Project/Audios Test Folder")
    videoSP = Path("C:/Users/andyr/OneDrive - Lehigh University/DESKTOP/Projects/Workstudy/Youtube-Downloader-Project/Videos Test Folder")
    combineSP = Path("C:/Users/andyr/OneDrive - Lehigh University/DESKTOP/Projects/Workstudy/Youtube-Downloader-Project/Combine Test Folder")
    link = input("Enter your link: ")
    combineAudioPath, combineVideoPath, fileName = downloadBoth(link, audioSP, videoSP)
    combineFiles(combineAudioPath, combineVideoPath, combineSP, fileName)
