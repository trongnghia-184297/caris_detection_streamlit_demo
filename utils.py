import os
import imghdr
import streamlit as st
from zipfile import ZipFile

def extract_zip(zip_path, destination_folder):
    with ZipFile(zip_path, 'r') as zip:
        zip.extractall(destination_folder)
    return zip.infolist()[0].filename

def check_folder(folder_path):
    # Check folder before predicting
    if not os.path.exists(folder_path):
        st.error("ERROR: Folder not found!")
        st.stop()

    if not os.listdir(folder_path):
        st.error("ERROR: No files found in the folder!")
        st.stop()
    else:
        check_image_folder(folder_path)
        st.info(
            f"Loading folder successfully. The folder contains \
                {len(os.listdir(folder_path))} images."
        )


def check_image_folder(folder_path):
    for img_name in os.listdir(folder_path):
        img_path = os.path.join(folder_path, img_name)
        if not os.path.isfile(img_path) or not imghdr.what(img_path):
            st.warning("Warning: Folder should contain only images.")
            st.error(f'ERROR: File "{img_path}" is not an image!')
            st.stop()


if __name__ == "__main__":
    # specifying the zip file name
    file_name = "/home/khanhhv2/workspace/test_images.zip"
    
    # opening the zip file in READ mode
    with ZipFile(file_name, 'r') as zip:
        # printing all the contents of the zip file
        print(zip.infolist()[0].filename)
    
        # extracting all the files
        print('Extracting all the files now...')
        zip.extractall()
        print('Done!')
