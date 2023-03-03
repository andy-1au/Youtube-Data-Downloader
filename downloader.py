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
    '''
    Get the video ID from the link
    :param link: (str)
    :return: video_id (str)
    '''
    video_id = link.split("?v=")[1] 
    if(video_id.find("&") != -1): 
        video_id = video_id.split("&")[0]
    return video_id

def CaptionDownload(video_id, channel_title):
    '''
    Download the transcript of the video and save it as a .txt file in SRT Format
    :param video_id: (str)
    :param video_title: (str)
    :return: None
    '''
    try:
        srt = YouTubeTranscriptApi.get_transcript("EGbONaJ8Im0", languages=['en']) # get transcript english only
        formatter = SRTFormatter() # format transcript to SRT format 
        savePath = os.path.join(transcriptSavePath, video_id+".txt")
        with open(savePath, "w") as srt_file:
            srt_file.write(formatter.format_transcript(srt))
    except:
        print("Error: Unable to download captions for video: " + video_id)
        with open(channel_title+"no_captions.txt", "a") as error_file:
            error_file.write(video_id + "\n")
        return None

def getChannelID(link):
    '''
    Get the channel ID from a link
    :param link: (str)
    :return: channel_id (str)
    '''
    video_id = getVideoID(link)
    channel_id = yt.get_video_metadata(video_id=video_id)['channel_id']
    return channel_id

def requestChannelData(link): # get channel ID from video ID using YouTubeDataAPI V3
    '''
    Send a GET request to the API to get the channel data using the channel ID
    :param link: (str)
    :return: None
    '''
    request = youtube.channels().list(
        part = "snippet,contentDetails",
        id = getChannelID(link), # get channel ID from video ID
    )
    response = request.execute()
    response = json.dumps(response, indent = 3, sort_keys=True) # convert to json format and sort by keys

async def requestVideoData(video_id): 
    '''
    (async) Send a GET request to the API to get the video data using the video ID
    :param video_id: (str)
    :return: response (dict)
    '''
    try:
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=video_id
        )
        response = request.execute()
        return response
    except:
        print("Error: Unable to get video data.")
            
def csvFormatter(video_data, video_id, csv_file, video_title):
    '''
    Format the video data to be saved in a csv file and save it in a folder
    :param video_data: (dict)
    :param video_title: (str)
    :param video_id: (str)
    :param csv_file: (str)
    :return: None
    '''
    data = video_data.get("items")[0]["snippet"]
    channel_title = data.get("channelTitle")
    video_publishedAt = data.get("publishedAt")
    video_thumbnail = data.get("thumbnails").get("high").get("url")
    video_description = data.get("description")
    
    if(video_description == ""):
        video_description = "No Description"
        
    if(video_id.find("=") != -1):
        video_id = video_id.split("=")[1]
        print(video_id)
        
    # write if to check if the video id starts with a - and add a ' in front of it
    if(video_id[0] == "-"):
        video_id = '"' + video_id + '"' # add quotes to the video id if it starts with a -
        print(video_id)

        
    # video_publishedAt = datetime.strptime(video_publishedAt, "%Y-%m-%dT%H:%M:%SZ")
    # video_publishedAt = video_publishedAt.strftime("%d/%m/%Y %I:%M:%S %p")
    
    with open(csv_file, "a", encoding="utf-8", newline='') as video_info:
        writer = csv.writer(video_info, delimiter=',',dialect='excel', quotechar='"', quoting=csv.QUOTE_NONE)
        csv_data = [channel_title, video_id, video_title, video_publishedAt, video_thumbnail, video_description]
        writer.writerow(csv_data)
    
def csv_file_creator(channel_title):
    '''
    Create a csv file to save the video data
    :param channel_title: (str)
    :return: csv_file (str)
    '''
    csv_headers = ["channel_title", "video_id","video_title", "video_publishedAt", "video_thumbnail", "video_description"]
    csv_file = os.path.join(video_infoPath, channel_title+".csv")
    with open(csv_file, "w", encoding="utf-8", newline='') as video_info:
        writer = csv.writer(video_info)
        writer.writerow(csv_headers)
    return csv_file

async def download(channel_id):
    '''
    (async) Download the video, transcript, and video info of the video. Send a GET request to the API to get the video data using the video ID and save it in a csv file in a folder
    :param channel_id: (str)
    :return: None
    '''
    
    request = youtube.channels().list(
        part="snippet,contentDetails",
        id= channel_id
    )
    
    response = request.execute()
    channel_title = response["items"][0]["snippet"]["title"]
    csv_file = csv_file_creator(channel_title)
    threads = [] # list of threads to run the async functions
    
    for item in response["items"]:
        playlist_id = item["contentDetails"]["relatedPlaylists"]["uploads"] # get the playlist ID of the uploads playlist
        next_page_token = '' # set the next page token to an empty string
        while(next_page_token != None): # while there is a next page token to get get the next 50 videos
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
                    
                    threadJson = threading.Thread(target=csvFormatter, args=(video_data, video_id, csv_file, video_title)) # start a thread to download the video info
                    threadCaption = threading.Thread(target= CaptionDownload, args=(video_id, channel_title)) # start a thread to download the transcript
                    threads.append(threadCaption)
                    threads.append(threadJson)
                    threadCaption.start()
                    threadJson.start()
                    
                    if 'nextPageToken' in playlistResponse.keys():
                        next_page_token = playlistResponse['nextPageToken']
                    else:
                        next_page_token = None

async def main():
    link = input("Enter the link to a youtube video: ")
    channel_id = getChannelID(link) # get channel ID from link
    await download(channel_id)# start downloading the videos, transcripts, and video info of the channel