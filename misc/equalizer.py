import os
import random
import shutil
import numpy as np

# Path to the dataset directory
data_path = "dataset/"
new_data_path = "dataset_balanced/"

# Create the new dataset directory if it doesn't exist
if not os.path.exists(new_data_path):
    os.makedirs(new_data_path)

# Get the list of subdirectories
subdirs = [os.path.join(data_path, d) for d in os.listdir(data_path) if os.path.isdir(os.path.join(data_path, d))]

# Count the number of files in each subdirectory
num_files_list = []
for subdir in subdirs:
    num_files = len([f for f in os.listdir(subdir) if os.path.isfile(os.path.join(subdir, f))])
    num_files_list.append(num_files)

# Determine the target number of files (minimum number of files across subdirectories)
target_files = min(num_files_list)

# For each subdirectory, duplicate or delete random files until it has the target number of files
for subdir in subdirs:
    # Create a corresponding subdirectory in the new dataset directory
    new_subdir = os.path.join(new_data_path, os.path.basename(subdir))
    if not os.path.exists(new_subdir):
        os.makedirs(new_subdir)

    # Copy all files from the original subdirectory to the new subdirectory
    files = [f for f in os.listdir(subdir) if os.path.isfile(os.path.join(subdir, f))]
    for file in files:
        shutil.copy(os.path.join(subdir, file), os.path.join(new_subdir, file))

    # Duplicate or delete random files until the new subdirectory has the target number of files
    num_files = len(files)
    while num_files < target_files:  # For oversampling
        file_to_duplicate = random.choice(files)
        new_file_name = os.path.splitext(file_to_duplicate)[0] + '_copy' + os.path.splitext(file_to_duplicate)[1]
        shutil.copy(os.path.join(subdir, file_to_duplicate), os.path.join(new_subdir, new_file_name))
        num_files += 1
    while num_files > target_files:  # For undersampling
        file_to_delete = random.choice(files)
        os.remove(os.path.join(new_subdir, file_to_delete))
        files.remove(file_to_delete)
        num_files -= 1