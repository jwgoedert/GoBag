from collections import defaultdict
import hashlib
import os
import time
import shutil
# Function to calculate the hash of a file


def hash_file(file_path):
    hasher = hashlib.md5()
    with open(file_path, 'rb') as file:
        while True:
            data = file.read(65536)  # Read in 64k chunks
            if not data:
                break
            hasher.update(data)
    return hasher.hexdigest()

# Function to find and identify duplicate files


def find_duplicates(start_directory):
    file_hashes = defaultdict(list)
    total_files = 0
    processed_files = 0

    for root, dirs, files in os.walk(start_directory):
        total_files += len(files)

    for filename in files:
        file_path = os.path.join(root, filename)
        file_hash = hash_file(file_path)
        file_hashes[file_hash].append(file_path)
        processed_files += 1
# Print progress every 100 files
        if processed_files % 100 == 0:
            print(f"Processed {processed_files}/{total_files} files...", end='\r')

# Create duplicates directory to store dupes before removal
    duplicates_dir = os.path.join(start_directory, "000duplicates000")
    os.makedirs(duplicates_dir, exist_ok=True)

# Move duplicates to the duplicates directory


# Print duplicates
    for hash_value, file_paths in file_hashes.items():
        if len(file_paths) > 1:
            print("Duplicate files (hash {}):".format(hash_value))
            original_file = file_paths[0]  # Keep the first occurrence
            for path in file_paths[1:]:
                print("  -", path)
                # Construct destination path in duplicates directory
                destination_path = os.path.join(duplicates_dir, os.path.basename(path))
                # Move duplicate File
                shutil.move(path, destination_path)
                print(f"   -Moved to duplicates directory: {destination_path}")


if __name__ == "__main__":
    # start_directory = "/path/to/your/root/directory"
    start_directory = input("What path would you like to survey?")
    
    # record start time
    start_time = time.time()

    find_duplicates(start_directory)

    # get end time, calculate and print end time
    end_time = time.time()
    overall_execution_time = end_time - start_time

    print(f"\nExecution time: {overall_execution_time} seconds")