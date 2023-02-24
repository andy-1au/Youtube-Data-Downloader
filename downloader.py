from datetime import datetime # for converting date
from youtube_api import YouTubeDataAPI                          # for getting youtube video data
from youtube_transcript_api import YouTubeTranscriptApi         # for getting transcript
from youtube_transcript_api.formatters import SRTFormatter      # for converting transcript to SRT format
from alive_progress import alive_bar                            # for progress bar

import os                           # for saving files
import googleapiclient.discovery    # what is the googleapiclient.discovery module? https://developers.google.com/youtube/v3/docs/playlists/list
import json                         # for converting to json format
import threading                    # for multithreading
import csv                          # for converting to csv format

videoSavePath = "/Users/dennis/Work Study/Special-Collections-Youtube-Downloader-Project/video" # Insert save path for videos here
audioSavePath = "/Users/dennis/Work Study/Special-Collections-Youtube-Downloader-Project/audio" # Insert save path for audio here
transcriptSavePath = "/Users/dennis/Work Study/Special-Collections-Youtube-Downloader-Project/transcript/" # Insert save path for transcript here
video_infoPath = "/Users/dennis/Work Study/Special-Collections-Youtube-Downloader-Project/video_info" # Insert save path for video info here

yt = YouTubeDataAPI("AIzaSyBXSsKWzuL06jQGffwrF_kAI75WGd2y5Rg")  # The YouTube Data API v3 service object to make requests to the API easier
youtube = googleapiclient.discovery.build("youtube", "v3", developerKey="AIzaSyBXSsKWzuL06jQGffwrF_kAI75WGd2y5Rg") # The YouTube Data API v3 service object to make actual requests to the API

def getVideoID(link):
    video_id = link.split("?v=")[1] # splits the link into a list and take the second element which is always the ID
    if(video_id.find("&") != -1): # if the video ID has a & in it it means there is a & with channel ID
        video_id = video_id.split("&")[0] # split the video ID by the & and take the first element which is always the video ID
    return video_id


def CaptionDownload(video_id, video_title):
    try:
        srt = YouTubeTranscriptApi.get_transcript(video_id, languages=['en']) # get transcript english only
        #formatter to convert transcript to SRT format
        formatter = SRTFormatter()
        savePath = os.path.join(transcriptSavePath, video_title+"_id:"+video_id+".txt")
        with open(savePath, "w") as srt_file:
            srt_file.write(formatter.format_transcript(srt))
    except:
        return None

def getChannelID(link): # get channel ID from video ID using YouTubeDataAPI
    video_id = getVideoID(link)
    channel_id = yt.get_video_metadata(video_id=video_id)['channel_id']
    return channel_id

def requestChannelData(link): # get channel ID from video ID using YouTubeDataAPI V3
    request = youtube.channels().list(
        part = "snippet,contentDetails",
        id = getChannelID(link),
    )
    response = request.execute()
    response = json.dumps(response, indent = 3, sort_keys=True) # convert to json format and sort by keys
    print(response)

async def requestVideoData(video_id): # get video data from video ID using YouTubeDataAPI V3 using async to speed up the process of getting video data
    try:
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=video_id
        )
        response = request.execute()
        return response
    except:
        print("Error: Unable to get video data.")

def csvFormatter(video_data, video_title, video_id):
    data = video_data.get("items")[0]["snippet"]
    channel_title = data.get("channelTitle")
    video_publishedAt = data.get("publishedAt")
    video_thumbnail = data.get("thumbnails").get("high").get("url")
    video_description = data.get("description")
    
    if(video_description == ""):
        video_description = "No Description"

    video_publishedAt = datetime.strptime(video_publishedAt, "%Y-%m-%dT%H:%M:%SZ") # convert date to datetime object to be able to format it 
    video_publishedAt = video_publishedAt.strftime("%d/%m/%Y %I:%M:%S %p") # format date to be more readable

    csv_headers = ["channel_title", "video_id","video_title", "video_publishedAt", "video_thumbnail", "video_description"]
    csv_data = [channel_title, video_id, video_title, video_publishedAt, video_thumbnail, video_description]
    if(video_title.find("/") != -1):
        video_title = video_title.replace("/", "-")
    else:
        savePath = os.path.join(video_infoPath, video_title+".csv")
        with open(savePath, "w", encoding="utf-16", newline='') as video_info:
            writer = csv.writer(video_info, delimiter="\t")
            writer.writerow(csv_headers)
            writer.writerow(csv_data)

async def download(channel_id):
    request = youtube.channels().list( # get request the channel data using the channel ID to get the play ID of the uploads playlist
        part="snippet,contentDetails",
        id= channel_id
    )
    
    response = request.execute()
    channel_title = response["items"][0]["snippet"]["title"]
    threads = [] # list of threads
    for item in response["items"]:
        # print(item)
        playlist_id = item["contentDetails"]["relatedPlaylists"]["uploads"] # get the playlist ID of the uploads playlist
        next_page_token = '' # set the next page token to an empty string
        while(next_page_token != None): # while there is a next page token to get get the next 50 videos
            # print("Next Page Token: ", next_page_token)
            playlistResponse = youtube.playlistItems().list(
                part="snippet",
                playlistId=playlist_id,
                maxResults=50,
                pageToken = next_page_token
            )
            playlistResponse = playlistResponse.execute()
            with alive_bar(len(playlistResponse['items'])) as bar:  # progress bar for downloading video transcript and video info
                for playlistItem in range(len(playlistResponse['items'])) and playlistResponse['items']:
                    bar()
                    video_id = playlistItem['snippet']['resourceId']['videoId']
                                     
                    with open(channel_title+".txt", "a") as video_id_file:
                        video_id_file.write(video_id+"\n")
                        
                    video_data = await requestVideoData(video_id) # start a thread to download the transcript
                    video_title = video_data["items"][0]["snippet"]["title"]
                    
                    threadJson = threading.Thread(target=csvFormatter, args=(video_data,video_title, video_id)) # start a thread to download the video info
                    threadCaption = threading.Thread(target= CaptionDownload, args=(video_id,video_title)) # start a thread to download the transcript
                    threads.append(threadCaption)
                    threads.append(threadJson)
                    threadCaption.start()
                    threadJson.start()
                    
                    if 'nextPageToken' in playlistResponse.keys():
                        next_page_token = playlistResponse['nextPageToken']
                    else:
                        next_page_token = None

async def main():
    link = input("Enter the link to a youtube video: ") # get link from user
    channel_id = getChannelID(link) # get channel ID from link
    await download(channel_id) # start downloading the videos

