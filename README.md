# Youtube Data Downloader

## Table of Contents
* [Overview](#overview)
    * [Description](#description)
    * [Features](#features)
    * [Specifications](#specifications)
    * [Technologies Used](#technologies-used)
    * [Challenges](#challenges)
    * [Future Implementations](#future-implementations)
* [Setting Up VSCode and Git](#setting-up-vscode-and-git)
* [Downloading Python and Pip](#downloading-python-and-pip)
* [Downloading External Dependencies](#downloading-external-dependencies)
    * [Getting ffmpeg](#getting-ffmpeg)
    * [Getting pytube](#getting-pytube)
    * [Getting OpenAI's Whisper](#getting-openais-whisper)
* [Install Make Using Chocolatey](#install-make-using-chocolatey)
* [Running the Application](#running-the-application)
    * [How to get youtube API Key](#how-to-get-youtube-api-key)
    * [How is the Youtube API Used](#how-is-the-youtube-api-used)       
    * [How is Metadata Saved](#how-is-metadata-saved)

## Overview 

>### Description

>> This project automates the process of downloading Youtube videos, metadata, and subtitles. Given a list of video IDs generated from Youtube's API, the Python script downloads the corresponding videos to a specified location. Using OpenAI's Whisper speech recognition model, the application transcribes the audio in each video to text and saves the transcript in a separate folder named after the video ID. Additionally, a CSV file is generated for each channel, containing specific metadata and video contents.

>### Features

* Downloads videos from Youtube using the video ID.
* Generates a CSV file for each channel, containing specific metadata and video contents.
* Transcribes the audio in each video to text using OpenAI's Whisper speech recognition model.
* Command line interface for easy use.

>### Specifications

* It is recommended that you use Windows for this. This was tested and built on Windows 10, but it should work on Windows 11 as well. 

* The script is designed to download YouTube content at the highest quality available. To achieve this, it utilizes the Pytube API to download the video and audio separately. This allows for the highest possible resolution and audio quality.

* Once the video and audio are downloaded, they are combined using ffmpeg. This encoding process ensures that the final output maintains the highest quality possible. The result is a video file that has both high video and audio quality, which is important for the end user's viewing experience.

* Additionally, the script includes error handling and validation to ensure that the downloaded content is valid and can be combined using ffmpeg. If an error occurs during the download or encoding process, the script provides helpful error messages to assist the user in troubleshooting the issue.

>### Technologies Used

* Python 3.8+ 
* ffmpeg and pytube APIs 
* os and subprocess Python libraries for threading
* OpenAI's Whisper speech recognition model

>### Challenges

* Ensuring that the correct video files were being downloaded and transcribed. We had to compare the list of video IDs provided to the files in the specified folder to make sure that we were transcribing the correct video files. 

* Running the application on certain NVIDIA GPU drivers, where threading was limited to only a few instances. We are still trying to implement a workaround to handle this limitation and ensure that the transcription process was still efficient.

* We had to experiment with different parameters and options in the Whisper model to improve the accuracy of the transcriptions.

* The video encoding process is limited by the system's current hardware. Using the default option (CPU) is usually slower, and in some cases, may not be able to encode videos at all. This is especially true for larger videos. Therefore, having a GPU is recommended for this process.

* The application is currently capped at 10,000 requests per day. This is due to the limitations of the Youtube API. We are currently looking into ways to increase this limit to allow for more videos to be downloaded.

>### Future Implementations

* Implement additional features to enhance user experience and expand the functionality of the application. These include developing a graphical user interface (GUI) to make the application more user-friendly and accessible to non-technical users. 

* Add support for more GPUs encoding formats, including AMD's GPU. 

* Aim to improve error handling and add more robust logging to enable users to troubleshoot any issues that arise during the video encoding process. 

* Explore the use of machine learning techniques to further improve the accuracy of the transcriptions, and to add support for more languages to make the application more widely accessible.

## Setting Up VSCode and Git 

1. Install [VScode](https://code.visualstudio.com/download) (Recommended) or Any alternative IDEs

2. Install [Git](https://git-scm.com/downloads) for bash, dependencies, and of course cloning this repo 

3. Launch VSCode, open your terminal with (crtl + ~). Make sure you are in the bash terminal (look at the very right of the terminal) 

4. PASTE in:

        git clone https://github.com/andy-1au/Special-Collections-Youtube-Downloader-Project.git

    Note: This step will clone the existing repository and will get you all of the most recent code, although, you won't be able to push to the remote repository 

    Note: When trying to match your local repository with the remote repository, type this in the terminal in the root folder of the repository: 
        
        git pull 

## Downloading Python and Pip

1. Download Python 3.9.7 from [here](https://www.python.org/downloads/release/python-397/). We recommend using the latest version of Python 3.9.7. because Whisper is only compatible with Python 3.8-3.10.

2. Install Python. Make sure to check the box that says "Add Python to PATH" during the installation process. This will allow you to run Python from the command line.

3. Verify that Python is installed correctly by running the following command in your terminal:

        python --version

4. If you see the version number of Python, then you have successfully installed Python. If you see an error message, then you may have to troubleshoot the issue.

5. In VSCode terminal, type this in git-bash:

        pip install -r requirements.txt

    NOTE: This will install all the dependencies needed for this project.

## Downloading External Dependencies

>### Getting ffmpeg

1. Download the latest version of [ffmpeg](https://ffmpeg.org/download.html) for your operating system. 
For Windows, you can download the latest version from [here](https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-full.7z). 
For Mac, you can download the latest version from [here](https://evermeet.cx/ffmpeg/ffmpeg-4.4.1.zip).

2. Extract the downloaded file to a location of your choice. We recommend extracting the file to Program Files on Windows, or to the root directory on Mac.

3. Add the location of the ffmpeg executable to your PATH environment variable. 
For Windows, you can follow the instructions [here](https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/). 
For Mac, you can follow the instructions [here](https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/).
Make sure to add 'C:\Program Files\ffmpeg\bin' to your PATH environment variable.

4. Verify that ffmpeg is installed correctly by running the following command in your terminal:

        ffmpeg -version

5. If you see the version number of ffmpeg, then you have successfully installed ffmpeg. If you see an error message, then you may have to troubleshoot the issue.

6. In VSCode terminal, type this in git-bash:

        pip install ffmpeg-python

    NOTE: ffmpeg-python is a Python wrapper for ffmpeg. It allows you to use ffmpeg in your Python scripts. 
    
    If you get an error, try this instead:

        pip3 install ffmpeg-python

7. Verify that ffmpeg-python is installed correctly by running the following command in your terminal:

        pip show ffmpeg-python

    NOTE: If you get an error, try this instead:

        pip3 show ffmpeg-python

>### Getting pytube

1. Pytube will be installed automatically when you run the following command in your terminal:

        pip install -r requirements.txt

2. But if you want to install it manually, run the following command in your terminal:

        pip install pytube

3. Verify that pytube is installed correctly by running the following command in your terminal:
    
        pip show pytube
    
4. This is the github repository link for [pytube](https://github.com/pytube/pytube), reference it if you need to troubleshoot any issues.

>### Getting OpenAI's Whisper

1. OpenAI's Whisper will be installed automatically when you run the following command in your terminal:

        pip install -r requirements.txt

2. But if you want to install it manually, run the following command in your terminal:

        pip install -U openai-whisper

3. Verify that OpenAI's Whisper is installed correctly by running the following command in your terminal:

        pip show openai-whisper
    
    NOTE: To update the package to the latest version of this repository, please run:

        pip install --upgrade --no-deps --force-reinstall git+https://github.com/openai/whisper.git

4. This is the github repository link for [OpenAI's Whisper](https://github.com/openai/whisper), reference it if you need to troubleshoot any issues.

## Install Make Using Chocolatey

1. Open PowerShell as Administrator and run:

        Set-ExecutionPolicy Bypass -Scope Process -Force; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

2. Verify that Chocolatey is installed correctly by running the following command in your terminal:

        choco --version

4. Install Make using Chocolatey by running the following command in your terminal:

        choco install make

5. Verify that Make is installed correctly by running the following command in your terminal:

        make --version

6. Lastly, restart your terminal or VSCode.

## Running the Application

1. Open the root folder of the repository in VSCode.

2. Open the terminal in VSCode and run the following command:

        make run

3. The application will start running and you will be prompted with a CLI menu.

4. Here are the main make commands that you can use:

    These commands are used to run the application. You can use them to run the application with or without a GUI. You can also use them to check if videos in the video folder are already downloaded by comparing the videos to a selected text file.

        make run
        make gui
        make check

    These commands are used to clean up the folders. You can use them if you want to delete the audio, video, or combined folders. You can also use them to create new folders.

        make clean
        make cleanAudio 
        make cleanVideo
        make cleanCombined
        make newFolder 

    NOTE: make newFolder will create a new folder in the root directory of the repository. You have to specify the name of the folder as an argument. For example, if you want to create a folder named 'test', then you would run the following command: 

        make newFolder name=test


>### How to get Youtube API Key

1. Create a Google Developer Account [here](https://developers.google.com/)

2. Create a new project

3. One the project's dashboard, click Explore & Enable APIs

4. In the library, navigate to YouTube Data APIv3 under YouTube APIs

5. Enable the API

6. Create a credential

7. You will be given a API key

>### Additional Information for Youtube API

Run the following command in your terminal to install the google-api-python-client for Python 3:

        pip install --upgrade google-api-python-client

Then include the following import statement as well as the code below it and replace the ? with you API-Key in your Python script:

        import googleapiclient.discovery 

        googleapiclient.discovery.build("youtube", "v3", developerKey="?") 

NOTE: Documentation for the YOUTUBE API V3 can be found [here](https://developers.google.com/youtube/v3/docs)

NOTE: Documentation for further start-up guidance can be found [here](https://developers.google.com/youtube/v3/quickstart/python)

>### How is the Youtube API used

1. Using the YouTubeData API we can extract video metadata and channel metadata from the YouTube Database we are able to call Web Requests to the Youtube API and get the data we need.

2. The API is capped at 10,000 requests per day, so we have to be careful with how many requests we make. If more request are needed contact YouTube for a higher limit. The link is procvided [here](https://support.google.com/youtube/contact/yt_api_form)

>### How is metadata Saved?

1. Metadata is saved as CSV format in the root directory of the repository. The name of the file is the name of the channel the video came from. For example, if the channel is named 'test', then the metadata will be saved in a file named 'test.csv'.

2. The information that is saved in the CSV file is the channel_title, video_id, video_title, video_publishedAt, video_thumbnail, video_description

## Credits and Acknowledgements

### Team Members
* Alex Japha - Project Manager
  * Responsible for overseeing project planning, management, and coordination.
* Andy Lau - Developer, Tester
  * Responsible for developing and implementing core video/audio downloading functions, including different types of video/audio formats, and video/audio conversion. 
  * Implemented the project's user interface and ensuring seamless integration with various third-party technologies.
  * Contributed to the development of the project's whisper audio transcription feature, utilizing advanced techniques to accurately transcribe audio files.
* Dennis Lam - Developer
   * Responsible for developing and implementing YOUTUBE API Web Requests to the Youtube Servers to get video metadata and channel metadata. Also scraped video transcripts in SRT format from Youtube.

## Copyright
© 2023, Andy Lau & Dennis Lam. All rights reserved. This project is licensed under the [MIT License](https://opensource.org/license/mit/). You are free to use and modify this project for personal or commercial purposes, provided that you give attribution to the original author and include the original license in any modified versions of the code.