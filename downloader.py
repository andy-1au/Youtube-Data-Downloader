from pytube import YouTube # for downloading videos
from pytube.cli import on_progress # for progress bar in terminal
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import SRTFormatter

from time import sleep
from tqdm import tqdm
import os

videoSavePath = "/Users/dennis/Work Study/Special-Collections-Youtube-Downloader-Project/video" #Insert save path for videos here

audioSavePath = "/Users/dennis/Work Study/Special-Collections-Youtube-Downloader-Project/audio" #Insert save path for audio here

transcriptSavePath = "/Users/dennis/Work Study/Special-Collections-Youtube-Downloader-Project/transcript/" #Insert save path for transcript here

def CaptionDownload(link):
    try:
        video_id = link.split("?v=")[1] # splits the link into a list and take the second element which is always the ID
        srt = YouTubeTranscriptApi.get_transcript(video_id, languages=['en']) # get transcript english only
        yt = YouTube(link)
        video_title = yt.title
        
        print("\nDownloading transcript...")
        for i in tqdm(range(10000)): # progress bar for transcript download
            sleep(0.0001)
        #formatter to convert transcript to SRT format
        formatter = SRTFormatter()
        savePath = os.path.join(transcriptSavePath, video_title+"_id:"+video_id+".txt")
        with open(savePath, "w") as srt_file:
            srt_file.write(formatter.format_transcript(srt))
    except:
        print('Error: Unable to download transcript.')
     
link = input('Enter the youtube link:')   
CaptionDownload(link)
