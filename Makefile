run:
	python Scripts/Download.py

gui: 
	python Scripts/GUI.py

removeAll:
	make removeAudio && make removeVideo && make removeCombined

removeAudio:
	cd Audios\ Folder/; \
	rm -rf -- * 

removeVideo:
	cd Videos\ Folder/; \
	rm -rf -- *

removeCombined:
	cd Combine\ Folder/; \
	rm -rf -- *