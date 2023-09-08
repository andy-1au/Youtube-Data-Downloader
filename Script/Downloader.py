import yt_dlp
import csv
import threading
import multiprocessing
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
    'subtitlesformat': 'srt',
    'writeautomaticsub': True,
}

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

def extract_metadata_threaded(metadata_put_path, video_id_list, channel_name):
    
    num_cpus = multiprocessing.cpu_count()

    num_threads = int(num_cpus*0.3)

    if(num_threads % 2 != 0):
        num_threads += 1

    thread = []

    deque_video_id = split_deque(video_id_list, num_threads) # n is the number of threads we want to use as well the number of parts we split the work load into
    
    if(metadata_put_path[-1] != '/'):
        metadata_put_path += '/'
        
    with open(metadata_put_path+channel_name+".csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer = writer.writerow(['id', 'title', 'description', 'date', 'thumbnail'])
    
    for i in range(len(deque_video_id)):
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
            data = dict(data)
            if(data.__contains__('entries')):
                for video in data['entries']:
                    txtfile.write(video['id']+'\n')
                    video_id.append(video['id'])
            else:
                txtfile.write(data['id']+'\n')
                video_id.append(data['id'])
                
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
        
def extract_captions(video_id_list, output_path, channel_name):
    
    if(output_path[-1] != '/'):
        output_path += '/' + channel_name + '/'
    
    for video in video_id_list:
        yt_dlp_captions_options['outtmpl'] = output_path+video
        ydl = yt_dlp.YoutubeDL(yt_dlp_captions_options)
        ydl.download(['https://www.youtube.com/watch?v='+video])

    
def main(channel_url, video_id_output_path, metadata_output_path, captions_output_path):
    result = extract_video_ids_threaded(channel_url, video_id_output_path)
    channel_name = result[0]
    video_id_list = result[1]
    extract_captions(video_id_list, captions_output_path, channel_name)
    extract_metadata_threaded(metadata_output_path, video_id_list, channel_name)
    