import os 

def compare(folderPath, txtFilePath):
    # read the video names from the txt file
    with open(txtFilePath, 'r') as f:
        videoIDs = f.read().splitlines()

    # get the video names from the folder
    videoFolderNames = []
    for fileName in os.listdir(folderPath):
        if fileName.endswith(".mp4"):
            videoFolderNames.append(fileName[:-4]) # remove the .mp4 extension

    # check if the folder contains the same videos as the txt file
    if set(videoIDs) == set(videoFolderNames):
        print("The folder contains the same videos as the txt file.")
    else:
        print("The folder does not contain the same videos as the txt file.")
        print("The following videos are missing:") # print the videos that are missing
        for id in videoIDs:
            if id not in videoFolderNames:
                print(id)

if __name__ == '__main__':

    # folder path 
    videoRootFolder = "Lehigh CAS"
    folderPath = videoRootFolder + "/Videos"

    # txt file path 
    txtFile = "Lehigh_University_College_of_Arts_and_Sciences.txt"
    txtFilePath = "ID Folder/" + txtFile

    compare(folderPath, txtFilePath)