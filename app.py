import streamlit as st
from ultralytics import YOLO
from scene.tab1 import tab1_scene
from scene.tab2 import tab2_scene


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

        # # Load model
        model = YOLO("checkpoints/best.pt")

        # Tab 1: predict a single image
        with tab1:
            tab1_scene(model=model)

        # Tab 2: predict a folder of images
        with tab2:
            tab2_scene(model)


if __name__ == "__main__":
    main()
