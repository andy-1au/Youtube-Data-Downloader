import whisper
import Download as dl   # Download.py


model = whisper.load_model("base") # load OpenAI's model

result = model.transcribe("Audios Folder\W-UusnlOxRM.mp4") 
lines = result['text'] # get the text
with open('Subtitles Folder\subtitle.txt', 'w') as f:
    f.write(lines)
print(result['text'])



