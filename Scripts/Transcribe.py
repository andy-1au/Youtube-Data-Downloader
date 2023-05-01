import whisper

model = whisper.load_model("base.en")

# Load the audio and transcribe it
result = model.transcribe("Audios Folder//ala.mp4", fp16=False)

# Print the text
print(result["text"])

# Print the text with timestamps
for line in result["lines"]:
    print(line["start"], line["end"], line["text"])





