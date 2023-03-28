import downloader as YOUTUBE_Downloader
import PySimpleGUI as sg

layout = [
        [sg.Text('Hello, World!')], 
        [sg.Button('-DOWNLOAD-')]
    ]
window = sg.Window('Youtube Downloader', layout, margins= (100, 100))

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == '-DOWNLOAD-':
        input = sg.popup_get_text('Enter Youtube Link')
        YOUTUBE_Downloader.asyncio.run(YOUTUBE_Downloader.main())

