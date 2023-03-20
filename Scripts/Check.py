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
        numMissing = 0
        missingIDs = []
        for id in videoIDs:
            if id not in videoFolderNames:
                print(id)
                numMissing += 1
                missingIDs.append(id)
            
        print(f"There are {numMissing} videos missing.")
    
    # write the missing videos to a txt file
    txtName = txtFile[:-4] + "_Missing Videos.txt"
    path = "ID Folder/" + txtName
    with open(path, 'w') as f:
        for id in missingIDs:
            f.write(id + "\n")
    
    print(f"The missing videos are written to {path}")

if __name__ == '__main__':

    # folder path 
    videoRootFolder = "Lehigh_University"
    folderPath = videoRootFolder + "/Videos"

    # txt file path 
    txtFile = "Lehigh University.txt"
    txtFilePath = "ID Folder/" + txtFile

    compare(folderPath, txtFilePath)