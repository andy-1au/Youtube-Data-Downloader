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

transcribe: 
	python Scripts/Transcribe.py

do_all:
	@if [ -z "$(folder)" ]; then \
		echo "Calls all targets (copy, info, transfer) in the correct order"; \
		echo "Usage: make move_folder folder=<folder_name>"; \
		exit 1; \
	fi
	$(MAKE) copy folder="$(folder)" && \
	$(MAKE) f_info folder="$(folder)" && \
	$(MAKE) vf_info folder="$(folder)" && \
	$(MAKE) transfer folder="$(folder)" 
	@echo "All targets completed"

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
	@echo "Main folders created"

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

copy:
	@if [ -z "$(folder)" ]; then \
		echo "Copies files from $(source_folder) to destination folder"; \
		echo "Usage: make copy folder=<destination_folder>"; \
		exit 1; \
	fi
	@echo "Transferring files from $(source_folder) to $(folder)/Videos"
	@mkdir -p "$(folder)/Videos"
	@mkdir -p "$(folder)/Metadata"
	@mkdir -p "$(folder)/Transcripts"
	@cp -r "$(source_folder)"/* "$(folder)/Videos"/ 
	@echo "Removing files from $(source_folder)"
	@$(MAKE) clean_combined 
	@echo "Transfer complete"

f_info:
	@if [ -z "$(folder)" ]; then \
		echo "Prints the number of files and total size of $(folder)"; \
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
		echo "Prints the number of files and total size of $(folder)/Videos"; \
		echo "Usage: make vf_info folder=<folder_path>"; \
		exit 1; \
	fi
	@echo "Checking number of files and total size of $(folder)/Videos"
	@file_count=`find "$(folder)/Videos" -type f | wc -l` && \
	total_size=`du -sh "$(folder)/Videos" | cut -f1` && \
	echo "Number of files: $$file_count" && \
	echo "Total size: $$total_size"

transfer:
	@if [ -z "$(folder)" ]; then \
		echo "Transfers folder from $(C_PATH) to $(D_PATH)"; \
		echo "Usage: make transfer folder=<folder_name>"; \
		exit 1; \
	fi
	@echo "Moving folder $(folder) from $(C_PATH) to $(D_PATH)"
	@mv "$(C_PATH)/$(folder)" "$(D_PATH)"
	@echo "Folder moved successfully"

clean:
	make clean_audio && make clean_video && make clean_combined && make clean_subtitles && make clean_transcripts
	@echo "All folders cleaned"

clean_audio:
	cd Audios\ Folder/; \
	rm -rf -- * 
	@echo "Audios Folder cleaned"

clean_video:
	cd Videos\ Folder/; \
	rm -rf -- *
	@echo "Videos Folder cleaned"

clean_combined:
	cd Combine\ Folder/; \
	rm -rf -- *
	@echo "Combined Folder cleaned"

clean_subtitles:
	cd Subtitles\ Folder/; \
	rm -rf -- *
	@echo "Subtitles Folder cleaned"

clean_transcripts:
	cd Transcripts\ Folder/; \
	rm -rf -- *
	@echo "Transcripts Folder cleaned"

help:
	@echo "Available targets:"
	@echo "  run_new           - Runs the Download2.py script"
	@echo "  run_old           - Runs the Download.py script"
	@echo "  gui               - Runs the GUI.py script"
	@echo "  check             - Runs the Check.py script"
	@echo "  transcribe        - Runs the Transcribe.py script"
	@echo "  do_all            - Calls all targets (copy, info, transfer) in the correct order"
	@echo "  main_folders      - Creates the main folders and adds them to .gitignore"
	@echo "  new_folder        - Creates a new folder with Transcripts, Videos, and Metadata subfolders"
	@echo "  copy              - Copies files from Combine Folder to a specified destination folder"
	@echo "  transfer          - Transfers a folder from C_PATH to D_PATH"
	@echo "  f_info            - Prints the number of files and total size of a specified folder"
	@echo "  vf_info           - Prints the number of files and total size of a specified folder's Videos subdirectory"
	@echo "  clean             - Cleans all folders (audio, video, combined, subtitles, transcripts)"
	@echo "  clean_audio       - Cleans the Audios Folder"
	@echo "  clean_video       - Cleans the Videos Folder"
	@echo "  clean_combined    - Cleans the Combine Folder"
	@echo "  clean_subtitles   - Cleans the Subtitles Folder"
	@echo "  clean_transcripts - Cleans the Transcripts Folder"
	@echo "  help              - Displays this help message"


