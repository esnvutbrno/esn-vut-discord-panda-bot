all:
	true

.ONESHELL:
download-memes:
	mkdir -p ./memecon-memes/
	cd ./memecon-memes/
	wget -i ./../data/memecon-memes-urls
	rename -f 's/\.jpg.*/.jpg/' *