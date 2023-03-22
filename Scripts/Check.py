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
        exit()
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
    
        txtName = txtFile[:-4] + "_Missing Videos.txt"
        path = "ID Folder/" + txtName
        
        userInput= input(f"Do you want to write the missing videos to a txt file? (y/n) ") #ask the user if they want to write the missing videos to a txt file
        while userInput.lower() != "y" and userInput.lower() != "n": # check if the user input is valid
            userInput = input("Please enter a valid input (y/n) ")
        if userInput.lower() != "y":
            exit()
        else:
            with open(path, 'w') as f: # write the missing videos to a txt file
                for id in missingIDs:   
                    f.write(id + "\n")
            print(f"The missing videos are written to {path}")

if __name__ == '__main__':

    # folder path 
    videoRootFolder = "Lehigh_CEDU"
    # folderPath = videoRootFolder + "/Videos"
    folderPath = "Combine Folder"

    # txt file path 
    txtFile = "Lehigh University College of Health.txt"
    txtFilePath = "ID Folder/" + txtFile

    compare(folderPath, txtFilePath)