import whisper

import Download as dl   # Download.py


model = whisper.load_model("base") # load OpenAI's model

def transcribe(videoPath, outputPath):
    result = model.transcribe(videoPath)
    lines = result['text'] # get the text
    with open(outputPath, 'w') as f:
        f.write(lines)

result = model.transcribe("Combine Folder\mJoTBkLkVyg.mp4")
print(result['text'])
lines = result['text'] # get the text
outputPath = "Subtitles Folder\subtitle.txt"
with open(outputPath, 'w') as f:
    f.write(lines)