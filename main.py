import pandas as pd
import logging
from io import BytesIO
import streamlit as st
import chardet
from database import insert_data, get_tables, get_table, get_table_schema, run_sql_query
from prompts import sql_prompt, qa_prompt
import ollama
from typing import Dict, Generator

log_file = f"app_logger.log"
logging.basicConfig(filename=log_file, level=logging.INFO)

if "selected_table" not in st.session_state:
    st.session_state.selected_table = 0

if "data" not in st.session_state:
    st.session_state.data = ""

if "current_dataset" not in st.session_state:
    st.session_state.current_dataset = "current_dataset"


def ollama_generator(model_name: str, messages: Dict) -> Generator:
    stream = ollama.chat(model=model_name, messages=messages, stream=True)
    for chunk in stream:
        yield chunk["message"]["content"]


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
        st.rerun()

    table_names = get_tables()

    selected_table = st.selectbox(
        "Select a table:", table_names, index=st.session_state.selected_table
    )

    if st.session_state.selected_table != table_names.index(selected_table):
        st.session_state.selected_table = table_names.index(selected_table)

        st.session_state.current_dataset = table_names[st.session_state.selected_table]

        st.session_state.data = get_table(selected_table)

        schema = get_table_schema(st.session_state.current_dataset)
        st.write(schema)

# TODO: ugly and bad
if question := st.chat_input("Ask a question!"):
    schema = get_table_schema(st.session_state.current_dataset)
    prompt = sql_prompt(question, schema)

    messages = []
    messages.append({"role": "system", "content": prompt})
    messages.append({"role": "user", "content": question})

    with st.chat_message("user"):
        st.markdown(question)

    response = ollama.chat(model="llama3", messages=messages)
    query = response["message"]["content"]

    logging.info(f"Query: {query}\n AI Response: {response}")

    result = run_sql_query(query)

    logging.info(f"Response: {result}")

    prompt = qa_prompt(question, query, result)

    # TODO: save history of messages
    messages = []
    messages.append({"role": "system", "content": prompt})

    with st.chat_message("assistant"):
        st.write(response)
        response = st.write_stream(
            ollama_generator(model_name="llama3", messages=messages)
        )
