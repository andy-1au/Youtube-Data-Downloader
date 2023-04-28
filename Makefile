C_PATH := /c/Special-Collections-Youtube-Downloader-Project
D_PATH := /d/Channels
source_folder := Combine Folder

run_new: 
	python Scripts/Download2.py

run_old:
	python Scripts/Download.py

gui: 
	python Scripts/GUI.py

check: 
	python Scripts/Check.py

main_folders:
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

new_folder:
	@if [ -z "$(name)" ]; then \
		echo "Usage: make new_folder name=<folder_name>"; \
		exit 1; \
	fi
	@echo "" >> .gitignore && \
	echo $(name) >> .gitignore && \
	mkdir "$(name)" && \
	cd "$(name)" && \
	mkdir Transcripts Videos Metadata
	@echo "New folder: $(name) created"

transfer:
	@if [ -z "$(dst)" ]; then \
		echo "Usage: make transfer dst=<destination_folder>"; \
		exit 1; \
	fi
	@echo "Transferring files from $(source_folder) to $(dst)/Videos"
	@mkdir -p "$(dst)/Videos"
	@mkdir -p "$(dst)/Metadata"
	@mkdir -p "$(dst)/Transcripts"
	@cp -r "$(source_folder)"/* "$(dst)/Videos"/ 
	@echo "Removing files from $(source_folder)"
	@$(MAKE) clean_combined 
	@echo "Transfer complete"

move_folder:
	@if [ -z "$(folder)" ]; then \
		echo "Usage: make move_folder folder=<folder_name>"; \
		exit 1; \
	fi
	@echo "Moving folder $(folder) from $(C_PATH) to $(D_PATH)"
	@mv "$(C_PATH)/$(folder)" "$(D_PATH)"
	@echo "Folder moved successfully"

f_info:
	@if [ -z "$(folder)" ]; then \
		echo "Usage: make f_info folder=<folder_path>"; \
		exit 1; \
	fi
	@echo "Checking number of files and total size of $(folder)"
	@file_count=`find "$(folder)" -type f | wc -l` && \
	total_size=`du -sh "$(folder)" | cut -f1` && \
	echo "Number of files: $$file_count" && \
	echo "Total size: $$total_size"

vf_info:
	@if [ -z "$(folder)" ]; then \
		echo "Usage: make vf_info folder=<folder_path>"; \
		exit 1; \
	fi
	@echo "Checking number of files and total size of $(folder)"
	@file_count=`find "$(folder)" -type f | wc -l` && \
	total_size=`du -sh "$(folder)" | cut -f1` && \
	echo "Number of files: $$file_count" && \
	echo "Total size: $$total_size"

clean:
	make clean_audio && make clean_video && make clean_combined && make clean_subtitles && make clean_transcripts

clean_audio:
	cd Audios\ Folder/; \
	rm -rf -- * 

clean_video:
	cd Videos\ Folder/; \
	rm -rf -- *

clean_combined:
	cd Combine\ Folder/; \
	rm -rf -- *

clean_subtitles:
	cd Subtitles\ Folder/; \
	rm -rf -- *

clean_transcripts:
	cd Transcripts\ Folder/; \
	rm -rf -- *