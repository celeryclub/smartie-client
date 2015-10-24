all: deploy

deploy:
	rsync -avP --exclude '/.git' --exclude '/.gitignore' --filter ':- .gitignore' . orange-wlan:~/smartie-client
