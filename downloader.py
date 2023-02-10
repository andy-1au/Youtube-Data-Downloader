from pytube import YouTube                  # for downloading videos
from youtube_api import YouTubeDataAPI      # for getting youtube video data
from pyyoutube import Api   # for getting youtube video data

from youtube_transcript_api import YouTubeTranscriptApi         # for getting transcript
from youtube_transcript_api.formatters import SRTFormatter      # for converting transcript to SRT format

from time import sleep      # for progress bar
from tqdm import tqdm       # for progress bar
import os, sys              # for saving files
import googleapiclient.discovery # what is the googleapiclient.discovery module? https://developers.google.com/youtube/v3/docs/playlists/list
import json                # for converting to json format

videoSavePath = "/Users/dennis/Work Study/Special-Collections-Youtube-Downloader-Project/video" # Insert save path for videos here

audioSavePath = "/Users/dennis/Work Study/Special-Collections-Youtube-Downloader-Project/audio" # Insert save path for audio here

transcriptSavePath = "/Users/dennis/Work Study/Special-Collections-Youtube-Downloader-Project/transcript/" # Insert save path for transcript here

video_infoPath = "/Users/dennis/Work Study/Special-Collections-Youtube-Downloader-Project/video_info" # Insert save path for video info here

api = Api(api_key="AIzaSyBXSsKWzuL06jQGffwrF_kAI75WGd2y5Rg")    # for getting youtube video data
yt = YouTubeDataAPI("AIzaSyBXSsKWzuL06jQGffwrF_kAI75WGd2y5Rg")  # make the get request to youtube easier to use
youtube = googleapiclient.discovery.build("youtube", "v3", developerKey="AIzaSyBXSsKWzuL06jQGffwrF_kAI75WGd2y5Rg") # this is for getting playlist data

def CaptionDownload(link):
    try:
        video_id = getVideoID(link) # splits the link into a list and take the second element which is always the ID
        srt = YouTubeTranscriptApi.get_transcript(video_id, languages=['en']) # get transcript english only
        yt = YouTube(link) # get video title
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

def getVideoID(link):
    video_id = link.split("?v=")[1] # splits the link into a list and take the second element which is always the ID
    return video_id

def getChannelID(link): # get channel ID from video ID using YouTubeDataAPI
    video_id = getVideoID(link)
    channel_id = yt.get_video_metadata(video_id=video_id)['channel_id']
    return channel_id

def getRequestPlaylistID(channel_id): # get playlist ID from video ID using YouTubeDataAPI V3
    request = youtube.playlists().list(
        part = "snippet",
        channelId = channel_id,
        maxResults = 50
    )
    response = request.execute()

    playlists = []
    while request is not None:
        response = request.execute()
        playlists += response['items']
        request = youtube.playlists().list_next(request, response)
    
    playlists_id = []
    for i in playlists:
        playlists_id.append(i['id'])
    
    return playlists_id

def getVideoID_from_playlist(playlist_id): # get video ID from playlist ID using YouTubeDataAPI V3
    x = yt.get_videos_from_playlist_id(playlist_id=playlist_id, count=1000)
    video_id = []
    for i in x: # get video ID from playlist ID
        video_id.append(i['video_id'])
    return video_id

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
    
request = youtube.channels().list(
    part="contentDetails",
    id= channel_id
)

response = request.execute()
for item in response["items"]:
    print(item)
    playlist_id = item["contentDetails"]["relatedPlaylists"]["uploads"]
    next_page_token = ''
    while(next_page_token != None):
        print("Next Page Token: ", next_page_token)
        playlistRespone = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            maxResults=50,
            pageToken = next_page_token
        )
        playlistResponse = playlistRespone.execute()
        for idx, playlistItem in enumerate(playlistResponse['items']):
            video_id = playlistItem['snippet']['resourceId']['videoId']
            video_data = requestVideoData(video_id)
            jsonFormatter(video_data)
            if 'nextPageToken' in playlistResponse.keys():
                next_page_token = playlistResponse['nextPageToken']
            else:
                next_page_token = None
