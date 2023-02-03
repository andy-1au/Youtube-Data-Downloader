from pyyoutube import Api # for getting youtube video data

from youtube_api import YouTubeDataAPI # for getting youtube video data
from youtube_api import parsers # for getting youtube video data

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import SRTFormatter

from time import sleep
from tqdm import tqdm

import json


YT_KEY = "AIzaSyBXSsKWzuL06jQGffwrF_kAI75WGd2y5Rg"
api = Api(api_key=YT_KEY)
yt = YouTubeDataAPI(YT_KEY)

channel_by_username = api.search_by_keywords(q="Lehigh University", search_type="channel", count=1)
json_channel = channel_by_username.items[0].to_json()
channel_id = json.loads(json_channel)['id']["channelId"]
print("Channel_Metadata: \n", json_channel)

print("Channel_ID: ",channel_id)

channel_metadata = yt.get_channel_metadata(channel_id=channel_id)
print("Channel_Metadata: ")
print(channel_metadata)

searches = yt.search(q="lehighuniversity", max_results=1)

video_id = parsers.raw_json(searches[0])['video_id']

print("Video_ID: "+video_id+"\n")
video_metadata = yt.get_video_metadata(video_id=video_id)
video_json = parsers.raw_json(video_metadata)
print(video_json["video_title"])

channel_metadata = yt.get_channel_metadata(channel_id=channel_id)
channel_json = parsers.raw_json(channel_metadata)
print(channel_json)