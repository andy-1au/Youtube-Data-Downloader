#Python Modules
from pathlib import Path
import os
import re # for regex

#Other Modules
from pytube import YouTube
from pytube.cli import on_progress  # for progress bar in terminal
import ffmpeg
import PySimpleGUI as sg

# Write parseID function here
def parseID(file):
    default_link = "https://www.youtube.com/watch?v="
    with open(file, 'r') as f: # 'with' closes the file for you
        id_list = [line.rstrip() for line in f] #removes the newline character from the end of each line
        link_list = [{default_link + id} for id in id_list] # creates a list of links from the list of ids
    # print(f"IDs: {id_list}") #DEBUG
    # print(f"Links: {link_list}") #DEBUG
    return link_list 

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

    except Exception as e:
        print('Error: Unable to download audio and video files:', e)
        return None


# Main Function 
if __name__ == '__main__':

    #NOTE: When using a new path, make sure to replace the backslash with forward slash. Relative pathing also works, and might be the best way to do it when testing the scripts
    parseID("video_ids.txt")

    # combineFiles(combineAudioPath, combineVideoPath, combineSP, fileName)
    # audioSP = Path("Insert Path Here")
    # videoSP = Path("Insert Path Here")
    # combineSP = Path("Insert Path Here")
    # audioSP = Path("C:/Users/andyr/OneDrive - Lehigh University/DESKTOP/Projects/Workstudy/Youtube-Downloader-Project/Audios Test Folder")
    # videoSP = Path("C:/Users/andyr/OneDrive - Lehigh University/DESKTOP/Projects/Workstudy/Youtube-Downloader-Project/Videos Test Folder")
    # combineSP = Path("C:/Users/andyr/OneDrive - Lehigh University/DESKTOP/Projects/Workstudy/Youtube-Downloader-Project/Combine Test Folder")
    # audioSP = Path("C:/Users/indigit/Desktop/Special-Collections-Youtube-Downloader-Project/Audios Test Folder")
    # videoSP = Path("C:/Users/indigit/Desktop/Special-Collections-Youtube-Downloader-Project/Videos Test Folder")
    # combineSP = Path("C:/Users/indigit/Desktop/Special-Collections-Youtube-Downloader-Project/Combine Test Folder")

    audioSP = Path("Audios Test Folder")
    videoSP = Path("Videos Test Folder")
    combineSP = Path("Combine Test Folder")
    # link = input("Enter your link: ")
    

    # combineAudioPath, combineVideoPath, fileName = downloadBoth(link, audioSP, videoSP)



#test comment 