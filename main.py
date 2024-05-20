import pandas as pd
from io import BytesIO
import sqlite3
import streamlit as st
import chardet


@st.experimental_dialog("Upload Data")
def show_upload_form():
    uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])
    filename = st.text_input("Filename", "")

    if st.button("Submit"):
        if filename and uploaded_file is not None:
            raw_data = uploaded_file.getvalue()
            result = chardet.detect(raw_data)
            encoding = result["encoding"]

            # TODO: Process data and store in DB
            data = pd.read_csv(BytesIO(raw_data), encoding=encoding)

            # st.write("Uploaded CSV File:")
            # st.dataframe(data)
        else:
            st.warning("Either uploaded file or filename is empty!")


st.title("AI Data Analytics")


with st.sidebar:
    upload_button = st.button("Upload Data")
    if upload_button:
        show_upload_form()
