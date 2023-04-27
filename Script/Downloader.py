import yt_dlp
import os
import csv
import threading
from collections import deque

yt_dlp_id_options = {
    'skip_download': True,
    'extract_flat': True,
    'skip_playlist_metadata': True,
}

yt_dlp_metadata_options = {
    'skip_download': True,
    'flat_playlist': True,
    'extract_flat': True,
}

yt_dlp_captions_options = {
    'skip_download': True,
    'extract_flat': True,
    'captions_only': True,
    'writeautomaticsub': True,
    'subtitlesformat': 'srt',
}
#dict_keys(['id', 'title', 'formats', 'thumbnails', 'thumbnail', 'description', 'uploader', 'uploader_id', 'uploader_url', 'channel_id', 'channel_url', 'duration', 'view_count', 'average_rating', 'age_limit', 'webpage_url', 'categories', 'tags', 'playable_in_embed', 'live_status', 'release_timestamp', '_format_sort_fields', 'automatic_captions', 'subtitles', 'comment_count', 'chapters', 'like_count', 'channel', 'channel_follower_count', 'upload_date', 'availability', 'original_url', 'webpage_url_basename', 'webpage_url_domain', 'extractor', 'extractor_key', 'playlist_count', 'playlist', 'playlist_id', 'playlist_title', 'playlist_uploader', 'playlist_uploader_id', 'n_entries', 'playlist_index', '__last_playlist_index', 'playlist_autonumber', 'display_id', 'fulltitle', 'duration_string', 'is_live', 'was_live', 'requested_subtitles', '_has_drm', 'requested_formats', 'format', 'format_id', 'ext', 'protocol', 'language', 'format_note', 'filesize_approx', 'tbr', 'width', 'height', 'resolution', 'fps', 'dynamic_range', 'vcodec', 'vbr', 'stretched_ratio', 'aspect_ratio', 'acodec', 'abr', 'asr', 'audio_channels'])

def extract_metadata(channel_url, output_path):
    """_summary_
        This function is slow, but it works. It extracts metadata from a channel and saves it to a csv file in the out put path.
    Args:
        channel_url (_type_): _description_
        output_path (_type_): _description_
    """
    
    ydl = yt_dlp.YoutubeDL(yt_dlp_metadata_options)
    
    metadata = ydl.extract_info(channel_url, download=False)

    channel = metadata['channel']
    
    if(output_path[-1] != '/'):
        output_path += '/'
    
    with open(output_path+channel+".csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer = writer.writerow(['id', 'title', 'description', 'date', 'thumbnail'])
    
    for data in metadata['entries']:
        
        id = data['id']
        title = data['title']
        description = data['description']
        date = data['upload_date']
        thumbnail = data['thumbnail']
        
        with open(output_path+channel+".csv", 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer = writer.writerow([id, title, description, date, thumbnail])
            
    return metadata

def extract_metadata_threaded(channel_url, metadata_put_path, id_file_output_path):
    thread = []

    result = extract_video_ids_threaded(channel_url, id_file_output_path)
    channel_name = result[0]
    video_id = deque(result[1])
    deque_video_id = split_deque(video_id, 8) # n is the number of threads we want to use as well the number of parts we split the work load into
    
    if(metadata_put_path[-1] != '/'):
        metadata_put_path += '/'
        
    if(id_file_output_path[-1] != '/'):
        id_file_output_path += '/'
        
    with open(metadata_put_path+channel_name+".csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer = writer.writerow(['id', 'title', 'description', 'date', 'thumbnail'])
    
    for i in range(len(deque_video_id)):
        print(i)
        thread.append(threading.Thread(target=extract_metadata_threaded_helper, args=(deque_video_id[i], metadata_put_path+channel_name+".csv")))
        thread[i].start()
    
def extract_metadata_threaded_helper(video_id_list, output_path):
    
    ydl = yt_dlp.YoutubeDL(yt_dlp_metadata_options)

    for id in video_id_list:
        url = 'https://www.youtube.com/watch?v='+id
        metadata = ydl.extract_info(url, download=False)
        
        id = metadata['id']
        title = metadata['title']
        description = metadata['description']
        date = metadata['upload_date']
        thumbnail = metadata['thumbnail']
        
        with open(output_path, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer = writer.writerow([id, title, description, date, thumbnail])
    
def split_deque(video_id, parts):
    video_ids = deque(video_id)
    
    part_size = len(video_ids) // parts
    
    result = []
    for i in range(parts):
        partition = [video_ids.popleft() for i in range(part_size)]
        result.append(partition)
    
    while video_ids:
        result[-1].append(video_ids.popleft())

    return result
    
def extract_video_ids_threaded(channel_url, output_path):
    ydl = yt_dlp.YoutubeDL(yt_dlp_id_options)
    metadata = ydl.extract_info(channel_url, download=False)
    
    result = [metadata['channel']]
    
    video_id = []
    
    print(output_path+metadata['channel']+".txt")
    
    if(output_path[-1] != '/'):
        output_path += '/'
    
    with open(output_path+metadata['channel']+".txt", 'w', newline='') as txtfile:
        for data in metadata['entries']:
            for video in data['entries']:
                txtfile.write(video['id']+'\n')
                video_id.append(video['id'])
                
    result.append(video_id)
    
    return result
    
def extract_video_id(metadata, output_path):
    channel = metadata['channel']
    
    if(output_path[-1] != '/'):
        output_path += '/'
    
    with open(output_path+channel+".txt", 'a', newline='') as txtfile:
        for data in metadata['entries']:
            if(data['id'][0] == '-'):
                data['id'] = "'"+data['id']+"'"
            txtfile.write(data['id']+'\n')
        
def extract_captions(video_id, output_path):
    
    if(output_path[-1] != '/'):
        output_path += '/'
        
    yt_dlp_captions_options['outtmpl'] = output_path
    
    ydl = yt_dlp.YoutubeDL(yt_dlp_captions_options)
    ydl.download(['https://www.youtube.com/watch?v='+video_id])
    

extract_metadata_threaded('https://www.youtube.com/channel/UC8butISFwT-Wl7EV0hUK0BQ', '/Users/dennis/Work Study/Special-Collections-Youtube-Downloader-Project/Metadata', '/Users/dennis/Work Study/Special-Collections-Youtube-Downloader-Project/IDS')