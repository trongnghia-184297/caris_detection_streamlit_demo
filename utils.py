import os
import imghdr
import streamlit as st


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
