import ffmpeg
import PySimpleGUI as sg

from pytube import YouTube
from pytube.cli import on_progress  # for progress bar in terminal

def combineFiles(audioPath, videoPath, combineSP):
    name = "January 2023 Message from President Joseph J. Helble"

    print("\nCombining audio and video files...")

    # input_video = ffmpeg.input("Videos Test Folder\\January 2023 Message from President Joseph J Helble.webm")
    # input_audio = ffmpeg.input("Audios Test Folder\\January 2023 Message from President Joseph J Helble.mp4")
    input_audio = ffmpeg.input(audioPath)
    input_video = ffmpeg.input(videoPath)
    ffmpeg.concat(input_video, input_audio, v=1, a=1).output(f"{combineSP}\\{name}.mp4").run(overwrite_output=True)
    # f"{combineSP}\\{name}.mp4"

def downloadBoth(link, audioSP, videoSP):
    videoObject = YouTube(link, on_progress_callback=on_progress)
    audioObject = YouTube(link, on_progress_callback=on_progress)
    try:
        print("\nDownloading Video File...")

        videoObject = videoObject.streams.filter(adaptive=True).order_by('resolution').desc().first()
        print(videoObject)  # debug
        videoName = videoObject.title
        # print(videoName) #debug
        # vtag = videoObject.itag #debug
        # print(str(vtag) + " is the itag of the video stream.") #debug
        videoObject.download(videoSP)

        print("\nDownloading Audio File..")
        audioObject = audioObject.streams.filter(only_audio=True).first()
        print(audioObject)  # debug
        audioName = audioObject.title
        # print(audioName) #debug
        # atag = audioObject.itag #debug
        # print(str(atag) + " is the itag of the audio stream.") #debug
        audioObject.download(audioSP)

        print("\nDownload complete.")

        return videoName, audioName
        # if I return this, can I use it in the combineFiles function?
        # I want to be able to pass the videoName and audioName to the combineFiles function.
        
    except:
        print('Error: Unable to download video.')

def downloadAudio(link, audioSP):
    audioObject = YouTube(link, on_progress_callback=on_progress)
    try:
        print("\nDownloading Audio File..")
        audioObject = audioObject.streams.filter(only_audio=True).first()
        print(audioObject)  # debug
        audioName = audioObject.title
        # print(audioName) #debug
        # atag = audioObject.itag #debug
        # print(str(atag) + " is the itag of the audio stream.") #debug
        audioObject.download(audioSP)

        print("\nDownload complete.")
    except:
        print('Error: Unable to download video.')

def downloadVideo(link, videoSP):
    videoObject = YouTube(link, on_progress_callback=on_progress)
    try:
        print("\nDownloading Video File...")

        videoObject = videoObject.streams.filter(adaptive=True).order_by('resolution').desc().first()
        print(videoObject)  # debug
        videoName = videoObject.title
        # print(videoName) #debug
        # vtag = videoObject.itag #debug
        # print(str(vtag) + " is the itag of the video stream.") #debug
        videoObject.download(videoSP)

        print("\nDownload complete.")
    except:
        print('Error: Unable to download video.')


def mainWindow():
    # Main Window
    sg.theme('DarkGrey9')
    layout = [
        [sg.T('Enter Youtube Links:'), sg.I(key='link')],
        [sg.T('Audio Format Save Path:'), sg.I(key='audioSP'), sg.FolderBrowse()],
        [sg.T('Video Format Save Path:'), sg.I(key='videoSP'), sg.FolderBrowse()],
        [sg.T('Combined Format Save Path:'), sg.I(key='combineSP'), sg.FolderBrowse()],
        [sg.T('Select Audio File'), sg.I(key='audioFile'), sg.FileBrowse()],
        [sg.T('Select Video File'), sg.I(key='videoFile'), sg.FileBrowse()],
        [sg.Button('Download Audio', key='downloadAudio'), sg.Button('Download Video', key='downloadVideo'),
         sg.Button('Download Both', key='downloadBoth'), sg.Button('Combine Files', key='combineFiles'), 
         sg.Button('Exit', key='exit')]
    ]
    window = sg.Window('Youtube Downloader', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'exit':
            break
        if event == 'downloadAudio':
            if values['link'] == '' or values['audioSP'] == '':
                sg.popup('Error: Please enter a link and/or save path.')
            else:
                downloadAudio(values['link'], values['audioSP'])
                sg.popup('Audio Download Complete')
        if event == 'downloadVideo':
            if values['link'] == '' or values['videoSP'] == '':
                sg.popup('Error: Please enter a link and/or save path.')
            else:
                downloadVideo(values['link'], values['videoSP'])
                sg.popip('Video Download Complete')
        if event == 'downloadBoth':
            if values['link'] == '' or values['audioSP'] == '' or values['videoSP'] == '':
                sg.popup('Error: Please enter a link and/or save path.')
            else:
                downloadBoth(values['link'], values['audioSP'], values['videoSP'])
                sg.popup('Both Download Complete')
        if event == 'combineFiles':
            if values['audioFile'] == '' or values['videoFile'] == '' or values['combineSP'] == '':
                sg.popup('Error: Please select the audio+video file and/or save path.')
            else:
                combineFiles(values['audioFile'], values['videoFile'], values['combineSP'])
                #center the popup window
                sg.popup('Combination Complete')

    window.close()

mainWindow()

