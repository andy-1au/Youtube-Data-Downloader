# Youtube Data Downloader

## Overview 

>### Description

>> This project automates the process of downloading Youtube videos, metadata, and subtitles. Given a list of video IDs generated from Youtube's API, the Python script downloads the corresponding videos to a specified location. Using OpenAI's Whisper speech recognition model, the application transcribes the audio in each video to text and saves the transcript in a separate folder named after the video ID. Additionally, a CSV file is generated for each downloaded video, containing specific metadata and video contents.

>### Specifications

> 1. The script is designed to download YouTube content at the highest quality available. To achieve this, it utilizes the Pytube API to download the video and audio separately. This allows for the highest possible resolution and audio quality.

> 2. Once the video and audio are downloaded, they are combined using ffmpeg. This encoding process ensures that the final output maintains the highest quality possible. The result is a video file that has both high video and audio quality, which is important for the end user's viewing experience.

> 3. Additionally, the script includes error handling and validation to ensure that the downloaded content is valid and can be combined using ffmpeg. If an error occurs during the download or encoding process, the script provides helpful error messages to assist the user in troubleshooting the issue.

>### Technologies Used

* Python 3.8+ 
* ffmpeg and pytube APIs 
* os and subprocess Python libraries for threading
* OpenAI's Whisper speech recognition model

>### Challenges

>1. Ensuring that the correct video files were being downloaded and transcribed. We had to compare the list of video IDs provided to the files in the specified folder to make sure that we were transcribing the correct video files. 

>2. Running the application on certain NVIDIA GPU drivers, where threading was limited to only a few instances. We are still trying to implement a workaround to handle this limitation and ensure that the transcription process was still efficient.

>3. We had to experiment with different parameters and options in the Whisper model to improve the accuracy of the transcriptions.

>4. The video encoding process is limited by the system's current hardware. Using the default option (CPU) is usually slower, and in some cases, may not be able to encode videos at all. This is especially true for larger videos. Therefore, having a GPU is recommended for this process. 

>### Future Features

>1. implement additional features to enhance user experience and expand the functionality of the application. These include developing a graphical user interface (GUI) to make the application more user-friendly and accessible to non-technical users. 

>2. Add support for more GPUs encoding formats, including AMD's GPU. 

>3. Aim to improve error handling and add more robust logging to enable users to troubleshoot any issues that arise during the video encoding process. 

>4. Explore the use of machine learning techniques to further improve the accuracy of the transcriptions, and to add support for more languages to make the application more widely accessible.


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


