import streamlit as st
import os
from ultralytics import YOLO
import cv2
import numpy as np


def main():
    """
    Main flow
    """
    # Check for page state
    st.session_state.page = "home"
    if st.session_state.page == "home":
        new_title = '<p style="font-size: 46px;">Welcome to Caries Recognition App!</p>'
        title = st.markdown(new_title, unsafe_allow_html=True)
        read_me = st.markdown(
            """
        This project was built by using Streamlit and ...

        To be continued...
                            """
        )

    # Create side bar with select box
    with st.sidebar.title("Select Activity"):
        st.sidebar.selectbox("MODE", ("About me", "App"), key="choices")
        st.session_state.page = st.session_state.choices

    # Run app scene
    if st.session_state.page == "App":
        title.empty()
        read_me.empty()
        app_scene()


def app_scene():
    """
    App scene
    """
    with st.container():
        # Title
        title_text = '<div style="text-align: center;"><p style="font-size: 36px;"> \
            Dental Caries Recognition</p></div>'
        st.markdown(title_text, unsafe_allow_html=True)

        # Create tabs for single image and image folder uploading
        listTabs = [
            "Single image",
            "Image folder",
        ]

        # Fills and centers each tab label with em-spaces
        whitespace = 32
        tab1, tab2 = st.tabs([s.center(whitespace, "\u2001") for s in listTabs])

        # Load model
        model = YOLO("checkpoints/best.pt")

        # st.session_state.tab = "tab1"
        # Tab 1: predict a single image
        with tab1:
            # Upload file
            uploaded_file = st.file_uploader(label="Upload single image")

            if uploaded_file is not None:
                image_byte = uploaded_file.read()
                np_array = np.frombuffer(image_byte, np.uint8)
                byte2arr = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
                img = cv2.cvtColor(byte2arr, cv2.COLOR_BGR2RGB)

                # Save image before predicting
                saved_folder = "saved/"
                if not os.path.exists(saved_folder):
                    os.makedirs(saved_folder, exist_ok=True)
                if len(os.listdir(saved_folder)) == 0:
                    newest_number_image = ""
                else:
                    newest_number_image = len(os.listdir(saved_folder)) + 1
                img_path = os.path.join(
                    saved_folder, f"img_test_{newest_number_image}.jpg"
                )
                cv2.imwrite(img_path, img)

                # Predict
                model.predict(
                    source=img_path, imgsz=960, save=True, conf=0.4, save_txt=False
                )

                # Load image from runs/segment/predict# folder
                runs_folder = "runs/segment"
                runs_lastest_num = len(os.listdir(os.path.join(runs_folder)))
                if runs_lastest_num == 1:
                    runs_lastest_num = ""
                predicted_img_name = os.listdir(
                    os.path.join(runs_folder, f"predict{runs_lastest_num}")
                )[0]
                predicted_img_path = os.path.join(
                    runs_folder, f"predict{runs_lastest_num}", predicted_img_name
                )
                predicted_img = cv2.imread(predicted_img_path)

                # Show result: origin and predicted images
                st.image(img, caption="Original image")
                st.image(predicted_img, caption="Predicted image")

        # Tab 2: predict a folder of images
        with tab2:
            # Upload folder of images
            folder_path = st.text_input("Enter Folder Path")
            if st.button("Upload Folder"):
                uploaded_file = None
                # Read and conver images to bytes from the folder
                # image_files = os.listdir(folder_path)

                # Predict
                model.predict(
                    source=folder_path,
                    imgsz=960,
                    save=True,
                    conf=0.4,
                    save_txt=False,
                )
                # Load image from runs/segment/predict# folder
                runs_folder = "runs/segment"
                runs_lastest_num = len(os.listdir(os.path.join(runs_folder)))
                if runs_lastest_num == 1:
                    runs_lastest_num = ""
                runs_latest_folder = os.path.join(
                    runs_folder, f"predict{runs_lastest_num}"
                )

                image_bytes = []
                for image_file in os.listdir(runs_latest_folder):
                    predicted_image_path = os.path.join(runs_latest_folder, image_file)
                    origin_image_path = os.path.join(folder_path, image_file)

                    with open(predicted_image_path, "rb") as file:
                        predicted_img = file.read()
                        image_bytes.append(predicted_img)

                    with open(origin_image_path, "rb") as file:
                        origin_img = file.read()
                        image_bytes.append(origin_img)

                # Display images with grid size n_cols x n_rows
                n_cols = 2
                n_rows = 1 + len(image_bytes) // int(n_cols)
                rows = [st.container() for _ in range(n_rows)]
                cols_per_row = [r.columns(n_cols) for r in rows]
                cols = [column for row in cols_per_row for column in row]

                for image_index, img in enumerate(image_bytes):
                    if image_index % 2 == 0:
                        cols[image_index].image(
                            img, caption=f"Original image {image_index + 1}"
                        )
                    else:
                        cols[image_index].image(
                            img, caption=f"Predicted image {image_index}"
                        )


if __name__ == "__main__":
    main()
