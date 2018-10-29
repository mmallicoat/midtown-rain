data/raw/response.txt:
	sh src/data/request_urls.sh

data/raw/images.csv data/raw/combined_urls.txt: data/raw/response.txt
	python src/data/extract_urls.py src/data

images:  # image files
	sh src/data/download_images.sh

data/interim/images.csv: data/raw/images.csv
	python src/data/add_labels.py data/raw data/interim
