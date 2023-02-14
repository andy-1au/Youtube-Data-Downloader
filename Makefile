run:
	python Scripts/Script.py

gui: 
	python Scripts/GUI.py

removeAll:
	make removeAudio && make removeVideo && make removeCombined

removeAudio:
	cd Audios\ Folder/; \
	rm -rf *.mp4

removeVideo:
	cd Videos\ Folder/; \
	rm -rf *.mp4

removeCombined:
	cd Combine\ Folder/; \
	rm -rf *.mp4