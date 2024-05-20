import pandas as pd
from io import BytesIO
import streamlit as st
import chardet
from database import insert_data, get_tables, get_table

if "selected_table" not in st.session_state:
    st.session_state.selected_table = 0

if "data" not in st.session_state:
    st.session_state.data = ""

@st.experimental_dialog("Upload Data")
def upload_data():
    uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])
    filename = st.text_input("Dataset Name", "")

    if st.button("Submit"):
        if filename and uploaded_file is not None:
            raw_data = uploaded_file.getvalue()
            result = chardet.detect(raw_data)
            encoding = result["encoding"]

            data = pd.read_csv(BytesIO(raw_data), encoding=encoding)

            insert_data(data, filename)

        else:
            st.warning("Either uploaded file or filename is empty!")


st.title("AI Data Analytics")


with st.sidebar:
    upload_button = st.button("Upload Data")
    if upload_button:
        upload_data()

    table_names = get_tables()
    selected_table = st.selectbox('Select a table:', table_names, index=st.session_state.selected_table)

    if st.session_state.selected_table != table_names.index(selected_table):
        st.session_state.selected_table = table_names.index(selected_table)
        st.session_state.data = get_table(selected_table)
        st.rerun()

    
