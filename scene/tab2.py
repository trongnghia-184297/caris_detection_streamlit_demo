import streamlit as st
from utils import check_folder
import time
import os

# import nicegui


def tab2_scene(model):
    # selected_folder = nicegui.directory_picker('Select a folder')

    # if selected_folder:
    # st.write("Selected folder:", selected_folder)

    # Upload folder of images
    folder_path = st.text_input("Enter Folder Path")
    if st.button("Upload Folder"):
        # Check folder before predicting
        check_folder(folder_path)

        # Download button
        st.button("Download")

        # Predict
        start_time = time.time()
        model.predict(
            source=folder_path,
            imgsz=960,
            save=True,
            conf=0.4,
            save_txt=False,
        )
        running_time = round(time.time() - start_time, 2)

        # Convert running time to 0.01-second intervals
        total_intervals = int(running_time * 100)
        # Progress bar
        prg = st.progress(0)

        for i in range(total_intervals):
            # Perform your tasks here.
            time.sleep(
                running_time / total_intervals
            )  # Adjust the delay based on running_time.

            # Calculate the percentage of completion
            progress_percent = (i + 1) / total_intervals

            # Update the progress bar with the calculated percentage
            prg.progress(progress_percent)

        # Show predicted time
        st.success(f"Prediction finished in {round(running_time, 2)}s", icon="✅")

        # Load image from runs/segment/predict# folder
        runs_folder = "runs/segment"
        runs_lastest_num = len(os.listdir(os.path.join(runs_folder)))
        if runs_lastest_num == 1:
            runs_lastest_num = ""
        runs_latest_folder = os.path.join(runs_folder, f"predict{runs_lastest_num}")

        image_bytes = []
        for image_file in os.listdir(runs_latest_folder):
            predicted_image_path = os.path.join(runs_latest_folder, image_file)
            origin_image_path = os.path.join(folder_path, image_file)

            with open(origin_image_path, "rb") as file:
                origin_img = file.read()
                image_bytes.append(origin_img)

            with open(predicted_image_path, "rb") as file:
                predicted_img = file.read()
                image_bytes.append(predicted_img)

        # Display images with grid size n_cols x n_rows
        n_cols = 2
        n_rows = 1 + len(image_bytes) // int(n_cols)
        rows = [st.container() for _ in range(n_rows)]
        cols_per_row = [r.columns(n_cols) for r in rows]
        cols = [column for row in cols_per_row for column in row]

        for image_index, img in enumerate(image_bytes):
            if image_index % 2 == 0:
                # Original image
                caption_index = image_index // 2 + 1
                cols[image_index].image(img, caption=f"Original image {caption_index}")
            else:
                # Predicted image
                caption_index = (image_index - 1) // 2 + 1
                cols[image_index].image(img, caption=f"Predicted image {caption_index}")
