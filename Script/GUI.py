import tkinter
from tkinter import filedialog
import customtkinter
import Downloader as dl
    
def select_directory(num):
    dir = filedialog.askdirectory()
    
    if(num == 1):
        video_output_path.set(str(dir))
        vidIDPath_selector.configure(text=video_output_path.get())
        vidIDPath_selector.update()
        print(video_output_path.get())
    elif(num == 2):
        metadata_output_path.set(str(dir))
        metadataPath_selector.configure(text=metadata_output_path.get())
        metadataPath_selector.update()
        print(video_output_path.get())
    elif(num == 3):
        caption_output_path.set(str(dir))
        captionPath_selector.configure(text=caption_output_path.get())
        captionPath_selector.update()
        print(video_output_path.get())
        
# System Settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# Our app frame
app = customtkinter.CTk()
app.geometry("720x480")
app.maxsize(width=500, height=400)
app.title("Youtube Downloader")

# Add UI Elements
title = customtkinter.CTkLabel(app, text="Insert a youtube channel link")
title.pack(padx=100, pady=10)

# Link input
url = tkinter.StringVar()
link = customtkinter.CTkEntry(app, width=350, height=40, textvariable=url)
link.pack()

# Directory Selector
dir_label = customtkinter.CTkLabel(app, text="VideoID-Output-Path")
dir_label.pack()

video_output_path = tkinter.StringVar()
vidIDPath_selector = customtkinter.CTkButton(app, text="select", command=lambda: select_directory(1))
vidIDPath_selector.pack()

dir_label1 = customtkinter.CTkLabel(app, text="Metadata-Output-Path")
dir_label1.pack()

metadata_output_path = tkinter.StringVar()
metadataPath_selector = customtkinter.CTkButton(app, text="select", command=lambda: select_directory(2))
metadataPath_selector.pack()

dir_label2 = customtkinter.CTkLabel(app, text="Caption-Output-Path")
dir_label2.pack()

caption_output_path = tkinter.StringVar()
captionPath_selector = customtkinter.CTkButton(app, text="select", command=lambda: select_directory(3))
captionPath_selector.pack()

# Download Button
download_button = customtkinter.CTkButton(app,
    text="Download", 
    command=lambda: dl.main(
        url.get(), 
        video_output_path.get(), 
        metadata_output_path.get(), 
        caption_output_path.get()
                     )
    )
download_button.pack(pady=25)

# Our app
app.mainloop()
