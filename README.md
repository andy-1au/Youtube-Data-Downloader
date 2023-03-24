# Youtube Data Downloader

## Overview 

>### Description

>> This project automates the process of downloading Youtube videos, metadata, and subtitles. Given a list of video IDs generated from Youtube's API, the Python script downloads thcorresponding videos to a specified location. Using OpenAI's Whisper speech recognition model, the application transcribes the audio in each video to text and saves the transcript in a separate folder named after the video ID. Additionally, a CSV file is generated for each downloaded video, containing specific metadata and video contents.

>### Specifications

> 1. The script is designed to download YouTube content at the highest quality available. To achieve this, it utilizes the Pytube API to download the video and audio separately. This allows for the highest possible resolution and audio quality.

> 2. Once the video and audio are downloaded, they are combined using ffmpeg. This encoding process ensures that the final output maintains the highest quality possible. The result is a video file that has both high video and audio quality, which is important for the end user's viewing experience.

> 3. Additionally, the script includes error handling and validation to ensure that the downloaded content is valid and can be combined using ffmpeg. If an error occurs during the download or encoding process, the script provides helpful error messages to assist the user in troubleshooting the issue.

>### Technologies Used

* Python 3.8+ 
* ffmpeg and pytube APIs 
* os and subprocess Python libraries for threading
* OpenAI's Whisper speech recognition model






## Setting Up VSCode and Git 
1. Install [VScode](https://code.visualstudio.com/download) (Recommended) or Any alternative IDEs

2. Install [Git](https://git-scm.com/downloads) for bash, dependencies, and of course cloning this repo 

3. Launch VSCode, open your terminal with (crtl + ~). Make sure you are in the bash terminal (look at the very right of the terminal) 

4. PASTE in:

        git clone https://github.com/andy-1au/Special-Collections-Youtube-Downloader-Project.git
    Note: This step will clone the existing repository and will get you all of the most recent code, although, you won't be able to push to the remote repository 

    Note: When trying to match your local repository with the remote repository, type this in the terminal in the root folder of the repository: 
        
        git pull 

## Downloading 


