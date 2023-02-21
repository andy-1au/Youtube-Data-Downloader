import whisper
import Download as dl   # Download.py


model = whisper.load_model("base") # load OpenAI's model

result = model.transcribe("Audios Folder\mJoTBkLkVyg.mp4")
print(result["text"])


def transcribe(videoPath, outputPath):
    result = model.transcribe(videoPath)
    lines = result['text'] # get the text
    with open(outputPath, 'w') as f:
        f.write(lines)

