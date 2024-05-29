import pandas as pd
import matplotlib.pyplot as plt
import logging
from io import BytesIO
import streamlit as st
import chardet
from data_analytics import (
    insert_data,
    get_tables,
    get_table_schema,
    run_sql_query,
    get_table_data,
)
from chat_instances import (
    create_database,
    update_chat_instance,
    add_chat_instance,
    get_chat_history,
    fetch_chats,
    delete_chat_instance,
)
from prompts import sql_prompt, qa_prompt
import ollama
from typing import Dict, Generator
from openai import OpenAI
import constants

log_file = f"app_logger.log"
logging.basicConfig(filename=log_file, level=logging.INFO)

if "selected_table" not in st.session_state:
    st.session_state.selected_table = 0

if "data" not in st.session_state:
    st.session_state.data = ""

if "current_dataset" not in st.session_state:
    st.session_state.current_dataset = ""

if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None

client = OpenAI(
    api_key=constants.OPENAI_API_KEY,
)


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


@st.experimental_dialog("View Data", width="large")
def view_data(table_name):
    st.header(table_name)
    df = get_table_data(table_name)
    st.write(df)


st.title("AI Data Analytics")

create_database()

get_chat_history()

with st.sidebar:
    upload_button = st.button("Upload Data")
    if upload_button:
        upload_data()
        st.rerun()

    if st.button("Create New Chat"):
        st.session_state.messages = []
        add_chat_instance()

    table_names = get_tables()

    selected_table = st.selectbox(
        "Select a table:", table_names, index=st.session_state.selected_table
    )

    if (st.session_state.selected_table != table_names.index(selected_table)) or (
        not st.session_state.current_dataset and len(table_names) > 0
    ):
        st.session_state.selected_table = table_names.index(selected_table)

        st.session_state.current_dataset = table_names[st.session_state.selected_table]

    if st.session_state.current_dataset:
        st.header(f"Curent Table: {st.session_state.current_dataset}")
        if st.button("View Data"):
            view_data(st.session_state.current_dataset)
            
    else:
        st.write(
            "No active table for chat. Please upload a CSV file to chat over data."
        )

    header = st.write(f"Active Chat: {st.session_state.current_chat_id}")

    # Sidebar for displaying chat instances
    chats = fetch_chats()

    for index, chat_id in enumerate(chats):
        button_label = f"Chat {chat_id[0]}"

        col1, col2 = st.columns(2)

        with col1:
            if st.button(button_label, help="Navigate to chat"):
                st.session_state.current_chat_id = chat_id[0]
                st.session_state.messages = get_chat_history()
                st.rerun()

        with col2:
            if st.button(
                "Delete Chat",
                key=f"{chat_id[0]}_{index}",
                help="Permanently delete chat, warning: unreversable!",
            ):
                delete_chat_instance(chat_id[0])

                if chat_id[0] == st.session_state.current_chat_id:
                    st.session_state.current_chat_id = None

                st.rerun()

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# TODO: ugly and bad
if question := st.chat_input("Ask a question!"):
    schema = get_table_schema(st.session_state.current_dataset)
    prompt = sql_prompt(question, schema)

    messages = []
    messages.append({"role": "system", "content": prompt})
    messages.append({"role": "user", "content": question})

    with st.chat_message("user"):
        st.markdown(question)

    completion = client.chat.completions.create(
        messages=messages,
        model="gpt-3.5-turbo",
    )
    query = completion.choices[0].message.content
    logging.info(f"Query: {query}")

    result = run_sql_query(query)

    logging.info(f"Response: {result}")

    prompt = qa_prompt(question, query, result)

    st.session_state.messages.append({"role": "system", "content": prompt})
    st.session_state.messages.append({"role": "user", "content": question})

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages,
            stream=True,
        )
        response = st.write_stream(stream)

    st.session_state.messages.append({"role": "assistant", "content": response})

    if len(st.session_state.messages) >= 3:
        update_chat_instance()
    else:
        add_chat_instance()
