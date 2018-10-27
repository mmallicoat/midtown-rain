urls.json:
	sh src/data/request_urls.sh

images.csv combined_urls.txt: urls.json
	py src/data/extract_urls.py src/data

images:
	sh src/data/download_images.sh
