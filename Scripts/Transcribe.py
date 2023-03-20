import whisper
import Download as dl   # Download.py


#https://www.assemblyai.com/blog/how-to-run-openais-whisper-speech-recognition-model/V

#text-davinci--002

model = whisper.load_model("base") # load OpenAI's model

# options = whisper.DecodingOptions(language='en', fp16=False)

result = model.transcribe("Audios Folder\W-UusnlOxRM.mp4") 
lines = result['text'] # get the text
with open('Subtitles Folder\subtitle.txt', 'w') as f:
    f.write(lines)
print(result['text']) 



