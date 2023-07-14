import streamlit as st
import os


def main():
    """
    Main flow
    """
    st.session_state.page = "home"
    if st.session_state.page == "home":
        new_title = '<p style="font-size: 46px;">Welcome to Caries Detection App!</p>'
        title = st.markdown(new_title, unsafe_allow_html=True)

        read_me = st.markdown(
            """
        This project was built by using Streamlit and ...

        To be continued...
                            """
        )

    with st.sidebar.title("Select Activity"):
        st.sidebar.selectbox("MODE", ("About me", "App"), key="choices")
        st.session_state.page = st.session_state.choices

    if st.session_state.page == "App":
        title.empty()
        read_me.empty()
        app_scene()


def app_scene():
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

        with tab1:
            uploaded_file = st.file_uploader(label="Upload single image")
            if uploaded_file is not None:
                image = uploaded_file.read()
                st.image(image, caption="Uploaded image", use_column_width=True)
        with tab2:
            # Upload folder of images
            folder_path = st.text_input("Enter Folder Path")
            if st.button("Upload Folder"):
                # Read images from the folder
                image_files = os.listdir(folder_path)

                # Convert image path to bytes
                image_bytes = []
                for image_file in image_files:
                    image_path = os.path.join(folder_path, image_file)
                    with open(image_path, "rb") as file:
                        image_data = file.read()
                        image_bytes.append(image_data)
                n_cols = 4
                n_rows = 1 + len(image_bytes) // int(n_cols)
                rows = [st.container() for _ in range(n_rows)]
                cols_per_row = [r.columns(n_cols) for r in rows]
                cols = [column for row in cols_per_row for column in row]

                for image_index, cat_image in enumerate(image_bytes):
                    cols[image_index].image(cat_image)


if __name__ == "__main__":
    main()
