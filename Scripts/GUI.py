from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from pathlib import Path
import os
import sys
import time
from datetime import timedelta
from concurrent.futures import ThreadPoolExecutor
import yt_dlp
from pathlib import Path

# Create the application instance
app = QApplication(sys.argv)

# Create the main window
window = QtWidgets.QMainWindow()

# Get the path of the stylesheet
ssPath = 'Scripts\stylesheet.qss'

# Read the stylesheet file
with open(ssPath, 'r') as f:
    stylesheet = f.read()

# Set the stylesheet of the widget to the contents of the file
window.setStyleSheet(stylesheet)

window.setWindowTitle("Youtube Data Downloader GUI")
window.setGeometry(200, 200, 500, 500) # x-coords, y-coords, width, height

# Create a central widget for the main window
central_widget = QWidget(window)
window.setCentralWidget(central_widget)

# Create a vertical layout for the central widget
layout = QVBoxLayout(central_widget)

# Create a label for the application title
title_label = QLabel("Youtube Data Downloader GUI")
title_label.setAlignment(QtCore.Qt.AlignCenter)
title_label.setFont(QtGui.QFont("Arial", 16))
layout.addWidget(title_label)

# Create a horizontal layout for the buttons
button_layout = QHBoxLayout()

# Create a button for downloading the video
download_button = QPushButton("Download Video")
download_button.setFixedHeight(50)
button_layout.addWidget(download_button)

# Create a button for playing the video
play_button = QPushButton("Play Video")
play_button.setFixedHeight(50)
button_layout.addWidget(play_button)

layout.addLayout(button_layout)

# Create a horizontal layout for the video player
video_layout = QHBoxLayout()

# Create a label for the video player
video_label = QLabel("Video Player")
video_label.setAlignment(QtCore.Qt.AlignCenter)
video_label.setFixedSize(400, 300)
video_layout.addWidget(video_label)

layout.addLayout(video_layout)

window.show()

app.exec_()