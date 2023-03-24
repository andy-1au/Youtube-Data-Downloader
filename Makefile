run:
	python Scripts/Download.py

gui: 
	python Scripts/GUI.py

check: 
	python Scripts/Check.py

newFolder:
	echo "" >> .gitignore && \
	echo $(name) >> .gitignore && \
	mkdir "$(name)" && \
	cd "$(name)" && \
	mkdir Transcripts Videos Metadata

clean:
	make cleanAudio && make cleanVideo && make cleanCombined

cleanAudio:
	cd Audios\ Folder/; \
	rm -rf -- * 

cleanVideo:
	cd Videos\ Folder/; \
	rm -rf -- *

cleanCombined:
	cd Combine\ Folder/; \
	rm -rf -- *