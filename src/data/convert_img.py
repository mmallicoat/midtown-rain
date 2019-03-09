from PIL import Image
import numpy as np
import pandas as pd
import pickle
import os
import pdb

# Convert images to grayscale and output as 3D array
def main():

    raw_dir = '/Users/user/Code/midtown-rain/data/raw'
    interim_dir = '/Users/user/Code/midtown-rain/data/interim'

    manifest = pd.read_csv(os.path.join(interim_dir, 'images.csv'))
    get_filename = lambda x: os.path.basename(x)
    filenames = manifest['image_path'].apply(get_filename)
    labels = manifest['rain']

    print("Process images...")
    image_list = list()
    for filename in filenames:
        # Convert to grayscale
        img = Image.open(os.path.join(raw_dir, filename)).convert('L')
        # Resize images to default size
        width, height = (960, 540)
        if img.size != (width, height):
            img = img.resize((width, height))
        # image bitmap has 8-bit color; use this to minimize size
        arr = np.array(img, dtype='int8')
        image_list.append(arr)

    print("Compile images...")
    train_data = np.stack(image_list)
    print("Save images to disk...")
    # Save images to pickle file
    with open(os.path.join(interim_dir, 'images.pkl'), 'w') as f:
        # Using pickle.dump causes bug, due to large size of array
        # pickle.dump(train_data, f, protocol=2)
        np.save(f, train_data, allow_pickle=True)
    print("Done.")

if __name__ == '__main__':
    main()
