import ffmpeg

from pytube import YouTube
from pytube.cli import on_progress  # for progress bar in terminal

#NOTE: This is a work in progress. I am still working on the combineFiles function. The combineFiles function is not working properly yet. I can't get it to take in file paths correctly. 

def combineFiles(audioPath, videoPath, combineSP):
    name = "January 2023 Message from President Joseph J. Helble"

    print("\nCombining audio and video files...")

    # input_video = ffmpeg.input("Videos Test Folder\\January 2023 Message from President Joseph J Helble.webm")
    # input_audio = ffmpeg.input("Audios Test Folder\\January 2023 Message from President Joseph J Helble.mp4")
    input_audio = ffmpeg.input(audioPath)
    input_video = ffmpeg.input(videoPath)
    ffmpeg.concat(input_video, input_audio, v=1, a=1).output(f"{combineSP}\\{name}.mp4").run(overwrite_output=True)
    # f"{combineSP}\\{name}.mp4"

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

        newAudioPath = f"{audioSP}\\{audioName}.mp4"
        newVideoPath = f"{videoSP}\\{videoName}.webm"

        return newAudioPath, newVideoPath
        
    except:
        print('Error: Unable to download video.')

# Main Function 
if __name__ == '__main__':
    audioSP = "C:\\Users\\andyr\\OneDrive - Lehigh University\\DESKTOP\\Projects\\Workstudy\\Special-Collections-Youtube-Downloader-Project\\Audios Test Folder"
    videoSP = "C:\\Users\\andyr\\OneDrive - Lehigh University\\DESKTOP\\Projects\\Workstudy\\Special-Collections-Youtube-Downloader-Project\\Videos Test Folder"
    combineSP = "C:\\Users\\andyr\\OneDrive - Lehigh University\\DESKTOP\\Projects\\Workstudy\\Special-Collections-Youtube-Downloader-Project\\Combine Test Folder"
    link = input("Enter your link: ")
    audioPath, videoPath = downloadBoth(link, audioSP, videoSP)
    combineFiles(audioPath, videoPath, combineSP)
