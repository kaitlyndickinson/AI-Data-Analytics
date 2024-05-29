import streamlit as st
import sqlite3
import json


def create_database():
    conn = sqlite3.connect("chat_instances.db")
    c = conn.cursor()

    c.execute(
        """CREATE TABLE IF NOT EXISTS ChatInstances 
                 (chat_history TEXT, thread_id INTEGER PRIMARY KEY AUTOINCREMENT)"""
    )

    conn.commit()
    conn.close()


def add_chat_instance():
    chat_history = st.session_state.messages[1:]

    # Serialize the updated chat history
    updated_chat_history = json.dumps(chat_history)

    conn = sqlite3.connect("chat_instances.db")
    c = conn.cursor()

    c.execute(
        """INSERT INTO ChatInstances (chat_history) 
                 VALUES (?)""",
        (updated_chat_history,)
    )

    thread_id = c.lastrowid

    st.session_state.current_chat_id = thread_id

    conn.commit()
    conn.close()


def update_chat_instance():
    chat_history = st.session_state.messages[1:]

    # Serialize the updated chat history
    updated_chat_history = json.dumps(chat_history)

    conn = sqlite3.connect("chat_instances.db")
    c = conn.cursor()

    c.execute(
        """UPDATE ChatInstances SET chat_history = ? WHERE thread_id = ?""",
        (updated_chat_history, st.session_state.current_chat_id),
    )

    conn.commit()
    conn.close()


def get_chat_history():
    conn = sqlite3.connect("chat_instances.db")
    c = conn.cursor()

    # Query to retrieve chat history based on username and chat ID
    c.execute(
        """SELECT chat_history FROM ChatInstances WHERE thread_id = ?""",
        (st.session_state.current_chat_id,)
    )

    # Fetch the first matching row
    chat_history = c.fetchone()

    conn.close()

    # Extract the chat history from the fetched row
    if chat_history:
        chat_history = json.loads(chat_history[0])
    else:
        chat_history = []

    return chat_history


# Function to delete a ChatThread instance given a thread_id
def delete_chat_instance(thread_id):
    conn = sqlite3.connect("chat_instances.db")
    c = conn.cursor()

    c.execute("""DELETE FROM ChatInstances WHERE thread_id = ?""", (thread_id,))

    thread_id = c.lastrowid

    if st.session_state.current_chat_id == thread_id:
        st.session_state.current_chat_id = None

    conn.commit()
    conn.close()

def fetch_chats():
    conn = sqlite3.connect("chat_instances.db")
    c = conn.cursor()

    # Fetch chats by username
    c.execute(
        "SELECT thread_id FROM ChatInstances"
    )
    chats = c.fetchall()

    conn.close()

    return chats