import downloader as YOUTUBE_DOWNLOADER
import asyncio


async def main(link):
    channel_id = YOUTUBE_DOWNLOADER.getChannelID(link) # get channel ID from link
    await YOUTUBE_DOWNLOADER.download(channel_id)# start downloading the videos, transcripts, and video info of the channel
        
while(True):
    
    link = input("Enter a YouTube link ( for the channel that you want to download ) : ")
    
    asyncio.run(main(link))
    
    if(input("Do you want to download another channel? (y/n) : ") == "n"):
        break
    else:
        continue