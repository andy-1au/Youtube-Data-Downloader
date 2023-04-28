runNew: 
	python Scripts/Download2.py

runOld:
	python Scripts/Download.py

gui: 
	python Scripts/GUI.py

check: 
	python Scripts/Check.py

folderInfo:
	@if [ -z "$(folder)" ]; then \
		echo "Usage: make folder_info folder=<folder_path>"; \
		exit 1; \
	fi
	@echo "Checking number of files and total size of $(folder)"
	@file_count=`find "$(folder)" -type f | wc -l` && \
	total_size=`du -sh "$(folder)" | cut -f1` && \
	echo "Number of files: $$file_count" && \
	echo "Total size: $$total_size"

videoFolderInfo
	if [ -z "$(folder)" ]; then \
		echo "Usage: make videoFolderInfo folder=<folder_path>"; \
		exit 1; \
	fi
	@echo "Checking number of files and total size of $(folder)"
	@file_count=`find "$(folder)" -type f -name "*.mp4" | wc -l` && \
	total_size=`du -sh "$(folder)" | cut -f1` && \
	echo "Number of files: $$file_count" && \
	echo "Total size: $$total_size"

mainFolders:
	mkdir -p Audios\ Folder && \
	mkdir -p Videos\ Folder && \
	mkdir -p Combine\ Folder && \
	mkdir -p Subtitles\ Folder && \
	mkdir -p Transcripts\ Folder && \
	mkdir -p Metadata\ Folder 
	echo "" >> .gitignore && \
	echo Audios\ Folder >> .gitignore && \
	echo Videos\ Folder >> .gitignore && \
	echo Combine\ Folder >> .gitignore && \
	echo Subtitles\ Folder >> .gitignore && \
	echo Transcripts\ Folder >> .gitignore && \
	echo Metadata\ Folder >> .gitignore

newFolder:
	@if [ -z "$(name)" ]; then \
		echo "Usage: make newFolder name=<folder_name>"; \
		exit 1; \
	fi
	@echo "" >> .gitignore && \
	echo $(name) >> .gitignore && \
	mkdir "$(name)" && \
	cd "$(name)" && \
	mkdir Transcripts Videos Metadata
	@echo "New folder: $(name) created"

transferFolder:
	@if [ -z "$(src)" ] || [ -z "$(dst)" ]; then \
		echo "Usage: make transferFolder src=<source_folder> dst=<destination_folder>"; \
		exit 1; \
	fi
	@echo "Transferring files from $(src) to $(dst)/Videos"
	@mkdir -p "$(dst)/Videos"
	@mkdir -p "$(dst)/Metadata"
	@mkdir -p "$(dst)/Transcripts"
	@cp -r "$(src)"/* "$(dst)/Videos"/ 
	@echo "Removing files from $(src)"
	@$(MAKE) cleanCombined 
	@echo "Transfer complete"


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
