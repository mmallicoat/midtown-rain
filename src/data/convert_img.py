from PIL import Image
import numpy as np
import pandas as pd
import pickle
import random
import os
import pdb

# Convert images to grayscale and output as 3D array
# and write out class labels
def main():

    raw_dir = '/Users/user/Code/midtown-rain/data/raw'
    interim_dir = '/Users/user/Code/midtown-rain/data/interim'
    processed_dir = '/Users/user/Code/midtown-rain/data/processed'

    manifest = pd.read_csv(os.path.join(interim_dir, 'images.csv'))
    get_filename = lambda x: os.path.basename(x)
    filenames = manifest['image_path'].apply(get_filename)
    labels = manifest['rain'].astype('uint8')

    # Get indices to stratify data into train, CV, and test
    n = len(filenames)
    n_train = int(.6 * n)
    n_cv = int(.2 * n)
    n_test = n - n_train - n_cv  # remainder is test data
    random.seed(666)  # set seed for reproducibility
    indices_train = random.sample(filenames.index, n_train)
    indices_cv = random.sample(filenames.index, n_cv)
    indices_test = random.sample(filenames.index, n_test)

    # Stratify
    filenames_train = filenames.ix[indices_train]
    filenames_cv = filenames.ix[indices_cv]
    filenames_test = filenames.ix[indices_test]
    labels_train = labels.ix[indices_train]
    labels_cv = labels.ix[indices_cv]
    labels_test = labels.ix[indices_test]

    # Process images
    train_data = process_images(filenames_train, raw_dir)
    cv_data = process_images(filenames_cv, raw_dir)
    test_data = process_images(filenames_test, raw_dir)

    print("Write out labels...")
    with open(os.path.join(processed_dir, 'train_labels.pkl'), 'w') as f:
        np.save(f, labels_train, allow_pickle=True)
    with open(os.path.join(processed_dir, 'cv_labels.pkl'), 'w') as f:
        np.save(f, labels_cv, allow_pickle=True)
    with open(os.path.join(processed_dir, 'test_labels.pkl'), 'w') as f:
        np.save(f, labels_test, allow_pickle=True)

    print("Save images to disk...")
    with open(os.path.join(processed_dir, 'train_data.pkl'), 'w') as f:
        np.save(f, train_data, allow_pickle=True)
    with open(os.path.join(processed_dir, 'cv_data.pkl'), 'w') as f:
        np.save(f, cv_data, allow_pickle=True)
    with open(os.path.join(processed_dir, 'test_data.pkl'), 'w') as f:
        np.save(f, test_data, allow_pickle=True)

    print("Done.")

def process_images(filenames, file_dir):
    print("Process images...")
    image_list = list()
    for filename in filenames:
        # Convert to grayscale
        img = Image.open(os.path.join(file_dir, filename)).convert('L')
        # Resize images to default size
        width, height = (960, 540)
        if img.size != (width, height):
            img = img.resize((width, height))
        # image bitmap has 8-bit color; use this to minimize size
        arr = np.array(img, dtype='uint8')
        image_list.append(arr)
    print("Compile images...")
    image_arr = np.stack(image_list)
    return image_arr
    
if __name__ == '__main__':
    main()
