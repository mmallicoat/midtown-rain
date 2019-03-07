from PIL import Image
import numpy as np
import pandas as pd
import os
import pdb

# Convert images to grayscale and output as 3D array
def main():

    image_dir = '/Users/user/Code/midtown-rain/data/raw'
    manifest_dir = '/Users/user/Code/midtown-rain/data/interim'

    manifest = pd.read_csv(os.path.join(manifest_dir, 'images.csv'))
    get_filename = lambda x: os.path.basename(x)
    filenames = manifest['image_path'].apply(get_filename)
    labels = manifest['rain']

    image_list = list()
    for filename in filenames[1:10]:
        # Open as grayscale
        img = Image.open(os.path.join(image_dir, filename)).convert('L')
        arr = np.array(img)
        # Pad to common dimensions with black pixels
        height, width = arr.shape  # rows, columns
        if width != 960:
            col = np.zeros((height, 960 - width))
            arr = np.concatenate((arr, row), axis=1)
        if height != 540:
            row = np.zeros((540 - height, 960))
            arr = np.concatenate((arr, row), axis=0)
        # Add as array to image list
        image_list.append(arr)

    train_data = np.stack(image_list)
    # save to pickle file

if __name__ == '__main__':
    main()

#        # Crop to common dimensions
#        width, height = img.size   # Get dimensions
#        if height != 540:
#            # White is 255; black is 0
#            pdb.set_trace()
#            left = 0
#            top = 0
#            right = 3 * width/4
#            bottom = 3 * height/4
#            # TODO
#            img.crop((left, top, right, bottom))
