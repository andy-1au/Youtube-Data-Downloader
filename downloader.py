from pytube import YouTube                  # for downloading videos
from youtube_api import YouTubeDataAPI      # for getting youtube video data
from pyyoutube import Api   # for getting youtube video data

from youtube_transcript_api import YouTubeTranscriptApi         # for getting transcript
from youtube_transcript_api.formatters import SRTFormatter      # for converting transcript to SRT format

from alive_progress import alive_bar        # for progress bar
import time                                 # for progress bar

import os           # for saving files
import googleapiclient.discovery # what is the googleapiclient.discovery module? https://developers.google.com/youtube/v3/docs/playlists/list
import json                # for converting to json format
import csv                 # for converting to csv format

videoSavePath = "/Users/dennis/Work Study/Special-Collections-Youtube-Downloader-Project/video" # Insert save path for videos here

audioSavePath = "/Users/dennis/Work Study/Special-Collections-Youtube-Downloader-Project/audio" # Insert save path for audio here

transcriptSavePath = "/Users/dennis/Work Study/Special-Collections-Youtube-Downloader-Project/transcript/" # Insert save path for transcript here

video_infoPath = "/Users/dennis/Work Study/Special-Collections-Youtube-Downloader-Project/video_info" # Insert save path for video info here

api = Api(api_key="AIzaSyBXSsKWzuL06jQGffwrF_kAI75WGd2y5Rg")    # for getting youtube video data
yt = YouTubeDataAPI("AIzaSyBXSsKWzuL06jQGffwrF_kAI75WGd2y5Rg")  # make the get request to youtube easier to use
youtube = googleapiclient.discovery.build("youtube", "v3", developerKey="AIzaSyBXSsKWzuL06jQGffwrF_kAI75WGd2y5Rg") # this is for getting playlist data

def getVideoID(link):
    video_id = link.split("?v=")[1] # splits the link into a list and take the second element which is always the ID
    return video_id

def CaptionDownload(video_id):
    try:
        srt = YouTubeTranscriptApi.get_transcript(video_id, languages=['en']) # get transcript english only
        video_title = requestVideoData(video_id)["items"][0]["snippet"]["title"]
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

def requestVideoData(video_id): # get video data from video ID using YouTubeDataAPI V3
    try:
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=video_id
        )
        response = request.execute()
    except:
        print("Error: Unable to get video data.")
    return response

link = input("Enter the link to a youtube video: ") # get link from user
 
channel_id = getChannelID(link) # get channel ID from link

def jsonFormatter(video_data):
    video_data = json.dumps(video_data, indent = 3, sort_keys=True) # convert to json format and sort by keys
    json_Data = json.loads(video_data).get("items")
    if(json_Data == []): # if the video is private, it will return an empty list
        print(json_Data)
    else:
        video_title = json_Data[0].get("snippet").get("title")
        if(video_title.find("/") != -1):
            video_title = video_title.replace("/", "-")
        savePath = os.path.join(video_infoPath, video_title+".json")
        with open(savePath, "w") as video_info:
            video_info.write(video_data)

request = youtube.channels().list( # get request the channel data using the channel ID to get the play ID of the uploads playlist
    part="contentDetails",
    id= channel_id
)

response = request.execute()
for item in response["items"]:
    # print(item)
    playlist_id = item["contentDetails"]["relatedPlaylists"]["uploads"] # get the playlist ID of the uploads playlist
    next_page_token = '' # set the next page token to an empty string
    while(next_page_token != None): # while there is a next page token to get get the next 50 videos
        # print("Next Page Token: ", next_page_token)
        playlistRespone = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            maxResults=50,
            pageToken = next_page_token
        )
        playlistResponse = playlistRespone.execute()
        with alive_bar(len(playlistResponse['items'])) as bar:  # progress bar for downloading video transcript and video info
            for playlistItem in range(len(playlistResponse['items'])) and playlistResponse['items']:
                bar()
                video_id = playlistItem['snippet']['resourceId']['videoId']
                video_data = requestVideoData(video_id)
                json_video_data = jsonFormatter(video_data)
                # convert jsonFormatter to CSV format
                
                caption = CaptionDownload(video_id)
                if(caption == None):
                    log = open("log.txt", "a") 
                    log.write("Error: Unable to download transcript for video id: "+video_id+"\n")
                if 'nextPageToken' in playlistResponse.keys():
                    next_page_token = playlistResponse['nextPageToken']
                else:
                    next_page_token = None
                time.sleep(0.001)
                
# next steps convert the json data to csv format with the correct schema
