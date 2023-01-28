from pytube import YouTube
from pytube.cli import on_progress # for progress bar in terminal

videoSavePath = "C://Users//andyr//OneDrive - Lehigh University//DESKTOP//Projects//Workstudy//Special-Collections-Youtube-Downloader-Project//Videos Test Folder" #Insert save path for videos here

audioSavePath = "C://Users//andyr//OneDrive - Lehigh University//DESKTOP//Projects//Workstudy//Special-Collections-Youtube-Downloader-Project//Audios Test Folder" #Insert save path for audio he

def DASHDownload(link): 
    videoObject = YouTube(link, on_progress_callback=on_progress)
    audioObject = YouTube(link, on_progress_callback=on_progress)
    try:
        print("\nDownloading Video File...")

        videoObject = videoObject.streams.filter(adaptive=True).order_by('resolution').desc().first()
        print(videoObject) # debug
        # vtag = videoObject.itag 
        # print(str(vtag) + " is the itag of the video stream.") #debug
        videoObject.download(videoSavePath)
        
        print("\nDownloading Audio File..")
        audioObject = audioObject.streams.filter(only_audio=True).first()
        print(audioObject) #debug
        # atag = audioObject.itag
        # print(str(atag) + " is the itag of the audio stream.") #debug
        audioObject.download(audioSavePath)
      
        print("\nDownload complete.")
    except:
        print('Error: Unable to download video.')

# Add function to combine audio and video files

link = input('Enter the youtube link:')
DASHDownload(link)