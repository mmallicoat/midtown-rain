urls-0.json:
	sh src/data/request_urls.sh

images.csv combined_urls.txt: urls-o.json
	py src/data/extract_urls.py
