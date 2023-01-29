import ffmpeg

from pytube import YouTube
from pytube.cli import on_progress  # for progress bar in terminal

from pathlib import Path

#NOTE: This is a work in progress. I am still working on the combineFiles function. The combineFiles function is not working properly yet. I can't get it to take in file paths correctly. 

def combineFiles(audioPath, videoPath, fileName, combineSP):
    
    print(f"fileName: {fileName}")

    print("\nCombining audio and video files...")

    input_audio = ffmpeg.input(audioPath)
    input_video = ffmpeg.input(videoPath)
    ffmpeg.concat(input_audio, input_video, v=1, a=1).output(f"{combineSP}\\{fileName}.mp4").run(overwrite_output=True)

def downloadBoth(link, audioSP, videoSP):
    videoObject = YouTube(link, on_progress_callback=on_progress)
    audioObject = YouTube(link, on_progress_callback=on_progress)
    try:
        print("\nDownloading Video File...")

        videoObject = videoObject.streams.filter(adaptive=True).order_by('resolution').desc().first()
        print(videoObject)  # debug
        videoName = videoObject.title
        # print(videoName) #debug
        # vtag = videoObject.itag #debug
        # print(str(vtag) + " is the itag of the video stream.") #debug
        videoObject.download(videoSP)

        print("\nDownloading Audio File..")
        audioObject = audioObject.streams.filter(only_audio=True).first()
        print(audioObject)  # debug
        audioName = audioObject.title
        # print(audioName) #debug
        # atag = audioObject.itag #debug
        # print(str(atag) + " is the itag of the audio stream.") #debug
        audioObject.download(audioSP)

        print("\nDownload complete.")

        newAudioPath = audioSP / f"{audioName}.mp4"
        newVideoPath = videoSP / f"{videoName}.mp4"

        return newAudioPath, newVideoPath, videoName

    except:
        print('Error: Unable to download video.')

# Main Function 
if __name__ == '__main__':
    audioSP = Path("C:/Users/andyr/OneDrive - Lehigh University/DESKTOP/Projects/Workstudy/Youtube-Downloader-Project/Audios Test Folder")
    videoSP = Path("C:/Users/andyr/OneDrive - Lehigh University/DESKTOP/Projects/Workstudy/Youtube-Downloader-Project/Videos Test Folder")
    combineSP = Path("C:/Users/andyr/OneDrive - Lehigh University/DESKTOP/Projects/Workstudy/Youtube-Downloader-Project/Combined Test Folder")
    link = input("Enter your link: ")
    combineAudioPath, combineVideoPath, fileName = downloadBoth(link, audioSP, videoSP)
    combineFiles(combineAudioPath, combineVideoPath, fileName, combineSP)
