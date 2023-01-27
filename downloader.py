from pytube import YouTube

videoSavePath = "C://Users//andyr//OneDrive - Lehigh University//DESKTOP//Projects//Workstudy//Special-Collections-Youtube-Downloader-Project//Videos Test Folder" #Insert save path for videos here

def Download(link):
    yt = YouTube(link)
    try: 
        print("Downloading...")
        yt.streams.filter(res="1080p").first().download('C://Users//andyr//OneDrive - Lehigh University//DESKTOP//Projects//Workstudy//Special-Collections-Youtube-Downloader-Project//Videos Test Folder')
        print("Download complete.")
    except:
        print('Error: Unable to download video.')
 
link = input('Enter the youtube link:')
Download(link)
