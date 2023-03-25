run:
	python Scripts/Download.py

gui: 
	python Scripts/GUI.py

check: 
	python Scripts/Check.py

mainFolders:
	mkdir -p Audios\ Folder && \
	mkdir -p Videos\ Folder && \
	mkdir -p Combine\ Folder && \
	mkdir -p Subtitles\ Folder && \
	mkdir -p Transcripts\ Folder && \
	mkdir -p Metadata\ Folder 

newFolder:
	echo "" >> .gitignore && \
	echo $(name) >> .gitignore && \
	mkdir "$(name)" && \
	cd "$(name)" && \
	mkdir Transcripts Videos Metadata

clean:
	make cleanAudio && make cleanVideo && make cleanCombined && make cleanSubtitles && make cleanTranscripts && make cleanMetadata

cleanAudio:
	cd Audios\ Folder/; \
	rm -rf -- * 

cleanVideo:
	cd Videos\ Folder/; \
	rm -rf -- *

cleanCombined:
	cd Combine\ Folder/; \
	rm -rf -- *

cleanSubtitles:
	cd Subtitles\ Folder/; \
	rm -rf -- *