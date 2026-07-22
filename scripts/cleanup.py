import os
import shutil

def clean_processed_data(folder="processed"):
    if os.path.exists(folder):
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            if os.path.isfile(file_path) and file_path.endswith(".npy"):
                os.remove(file_path)
        print(f"Cleaned up {folder} directory.")

if __name__ == "__main__":
    clean_processed_data()