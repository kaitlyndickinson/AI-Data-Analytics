import sqlite3
import json
import logging
import streamlit as st


def create_database():
    """
    Creates the SQLite database if it doesn't exist and initializes the ChatInstances table.
    Used to store separate chat instances so users can navigate between chats.

    Returns:
    None
    """
    try:
        conn = sqlite3.connect("chat_instances.db")
        c = conn.cursor()

        c.execute(
            """CREATE TABLE IF NOT EXISTS ChatInstances 
                     (chat_history TEXT, thread_id INTEGER PRIMARY KEY AUTOINCREMENT)"""
        )

        conn.commit()
    except Exception as e:
        logging.exception(f"Error creating database: {e}")
    finally:
        conn.close()


def add_chat_instance():
    """
    Adds a new chat instance to the ChatInstances table.

    Returns:
    None
    """
    try:
        # Exclude System prompt
        chat_history = st.session_state.messages[1:]

        updated_chat_history = json.dumps(chat_history)

        conn = sqlite3.connect("chat_instances.db")
        c = conn.cursor()

        c.execute(
            """INSERT INTO ChatInstances (chat_history) 
                     VALUES (?)""",
            (updated_chat_history,),
        )

        thread_id = c.lastrowid

        st.session_state.current_chat_id = thread_id
        conn.commit()
    except Exception as e:
        logging.exception(f"Error adding new chat instance: {e}")
    finally:
        conn.close()


def update_chat_instance():
    """
    Updates an existing chat instance in the ChatInstances table.

    Returns:
    None
    """
    try:
        # Exclude System prompt
        chat_history = st.session_state.messages[1:]

        updated_chat_history = json.dumps(chat_history)

        conn = sqlite3.connect("chat_instances.db")
        c = conn.cursor()

        c.execute(
            """UPDATE ChatInstances SET chat_history = ? WHERE thread_id = ?""",
            (updated_chat_history, st.session_state.current_chat_id),
        )

        conn.commit()
    except Exception as e:
        logging.exception("Error updating chat instance:")
    finally:
        conn.close()


def get_chat_history():
    """
    Retrieves the chat history for the current chat instance.

    Returns:
    list: A list of messages representing the chat history.
    """
    try:
        conn = sqlite3.connect("chat_instances.db")
        c = conn.cursor()

        c.execute(
            """SELECT chat_history FROM ChatInstances WHERE thread_id = ?""",
            (st.session_state.current_chat_id,)
        )

        chat_history = c.fetchone()
    except Exception as e:
        logging.exception(f"Error fetching chat history: {e}")
    finally:
        conn.close()

    if chat_history:
        chat_history = json.loads(chat_history[0])
    else:
        chat_history = []

    return chat_history


def delete_chat_instance(thread_id):
    """
    Deletes a chat instance from the ChatInstances table.

    Parameters:
    thread_id (int): The thread ID of the chat instance to delete.

    Returns:
    None
    """
    try:
        conn = sqlite3.connect("chat_instances.db")
        c = conn.cursor()

        c.execute("""DELETE FROM ChatInstances WHERE thread_id = ?""", (thread_id,))

        if st.session_state.current_chat_id == thread_id:
            st.session_state.current_chat_id = None

        conn.commit()
    except Exception as e:
        logging.exception(f"Error deleting chat instance: {e}")
    finally:
        conn.close()


def fetch_chats():
    """
    Fetches all chat instances from the ChatInstances table.

    Returns:
    list: A list of thread IDs representing the chat instances.
    """
    try:
        conn = sqlite3.connect("chat_instances.db")
        c = conn.cursor()

        c.execute(
            "SELECT thread_id FROM ChatInstances"
        )
        chats = c.fetchall()
    except Exception as e:
        logging.exception("Error fetching chats:")
    finally:
        conn.close()

    return chats
