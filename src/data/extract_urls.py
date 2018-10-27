import os
import sys
import json
import pdb
import pandas as pd

def main(argv):
    jsondir = os.path.abspath(argv[1])  # ./data/raw
    outdir = jsondir

    image_list = list()
    with open(os.path.join(jsondir, 'response.txt'), 'r') as f:
        json_list = f.read().splitlines()
    # NOTE: This is a list of valid JSON strings
    for json_str in json_list:
        response = json.loads(json_str[3:])  # remove Byte Order Mark
        for image in response['hofdata']:
            image_list.append(image)

    df = pd.DataFrame.from_dict(image_list)
    df.to_csv(os.path.join(outdir, 'images.csv'), index=False,
              encoding='utf-8')
    df['image_source'].to_csv(os.path.join(outdir, 'combined_urls.txt'),
                              index=False, encoding='utf-8')

if __name__ == '__main__':
    main(sys.argv)

