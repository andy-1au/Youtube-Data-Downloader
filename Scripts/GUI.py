from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from pathlib import Path
import os
import sys
import time
from datetime import timedelta
from concurrent.futures import ThreadPoolExecutor
import yt_dlp

# Create the application instance
app = QApplication(sys.argv)

window = QtWidgets.QMainWindow()
window.setWindowTitle("Youtube Data Downloader GUI")
window.setGeometry(100, 100, 500, 500)
# set color of window to blue
window.setStyleSheet("background-color: blue;")
window.show()

app.exec_()