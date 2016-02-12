all: deploy

deploy:
	rsync -avP --exclude '/.git' --exclude '/.gitignore' --filter ':- .gitignore' . orange:~/smartie-client
