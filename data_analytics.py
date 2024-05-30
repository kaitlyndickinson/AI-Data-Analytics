import sqlite3
import re
import logging
import pandas as pd


def get_dtype(dtype):
    """
    Returns the corresponding SQL data type for a given pandas dtype.

    Parameters:
    dtype (str): The pandas data type.

    Returns:
    str: The corresponding SQL data type.
    """
    if dtype == "Int64" or dtype == "int64":
        return "INTEGER"
    elif dtype == "Float64" or dtype == "float64":
        return "REAL"
    elif dtype == "boolean":
        return "BOOLEAN"
    else:
        return "TEXT"


def sanitize(name):
    """
    Sanitizes a string to remove non-alphanumeric characters.

    Parameters:
    name (str): The string to sanitize.

    Returns:
    str: The sanitized string.
    """
    return re.sub(r"\W+", "", name)


def insert_data(data, table_name):
    """
    Inserts data into an SQLite table, creating the table if it doesn't exist.

    Parameters:
    data (DataFrame): The pandas DataFrame containing the data to insert.
    table_name (str): The name of the table to insert the data into.
    """
    try:
        conn = sqlite3.connect("data_analytics.db")
        cursor = conn.cursor()

        data_types = data.dtypes.apply(lambda x: x.name).to_dict()

        columns = [
            (
                f"`{sanitize(col)}` {get_dtype(data_types[col])}"
                if "(" in col
                else f"{sanitize(col).replace('Group', '`Group`')} {get_dtype(data_types[col])}"
            )
            for col in data.columns
        ]

        table_name = sanitize(table_name)

        create_table_query = (
            f'CREATE TABLE IF NOT EXISTS {table_name} ({", ".join(columns)});'
        )

        cursor.execute(create_table_query)

        for row in data.itertuples(index=False, name=None):
            placeholders = ", ".join(["?" for _ in row])
            insert_query = f"INSERT INTO {table_name} VALUES ({placeholders});"
            cursor.execute(insert_query, row)

        conn.commit()
        conn.close()
    except Exception as e:
        logging.exception(f"Error inserting data into database: {e}")


def get_tables():
    """
    Retrieves the names of all tables in the SQLite database.

    Returns:
    list: A list of table names. None if an exception occurs.
    """
    try:
        conn = sqlite3.connect("data_analytics.db")
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        table_names = [table[0] for table in tables]
        return table_names
    except Exception as e:
        logging.exception(f"Error retrieving list of tables: {e}")
        return None


def get_table(table_name):
    """
    Retrieves all data from a specified table.

    Parameters:
    table_name (str): The name of the table to retrieve data from.

    Returns:
    list: A list of tuples representing the rows in the table. None if an exception occurs.
    """
    try:
        conn = sqlite3.connect("data_analytics.db")
        cursor = conn.cursor()

        cursor.execute(f"SELECT * FROM {table_name};")
        data = cursor.fetchall()

        conn.close()
        return data
    except Exception as e:
        logging.exception(f"Error getting {table_name}: {e}")
        return None


def run_sql_query(query):
    """
    Executes a given SQL query and returns the result.

    Parameters:
    query (str): The SQL query to execute.

    Returns:
    list: A list of tuples representing the rows returned by the query. None if an exception occurs.
    """
    try:
        conn = sqlite3.connect("data_analytics.db")
        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()

        conn.close()
        return data
    except Exception as e:
        logging.info(f"Error executing query: {query}, {e}")
        return None
   


def get_table_schema(table_name):
    """
    Retrieves the schema of a specified table.

    Parameters:
    table_name (str): The name of the table to get the schema for.

    Returns:
    str: A formatted string representing the table schema. None if an exception occurs.
    """
    try:
        conn = sqlite3.connect("data_analytics.db")
        cursor = conn.cursor()

        cursor.execute(f"PRAGMA table_info({table_name});")

        schema = cursor.fetchall()
        formatted_schema = format_table_scheme(schema, table_name)

        conn.close()
        return formatted_schema
    except Exception as e:
        logging.info(f"Error getting table schema for: {table_name}: {e}")
        return None
    


def format_table_scheme(schema, table_name):
    """
    Formats the schema information of a table into a readable string.

    Parameters:
    schema (list): The schema information retrieved from the database.
    table_name (str): The name of the table.

    Returns:
    str: A formatted string representing the table schema.
    """
    formatted_schema = f"Table name: {table_name}\n"

    for column in schema:
        formatted_schema += f"Column Name: {column[1]}\n"
        formatted_schema += f"Data Type: {column[2]}\n"
        formatted_schema += f"Not Null: {'Yes' if column[3] else 'No'}\n"
        formatted_schema += f"Default Value: {column[4]}\n"
        formatted_schema += f"Primary Key: {'Yes' if column[5] else 'No'}\n\n"

    return formatted_schema


def get_table_data(table_name):
    """
    Retrieves data from a specified table and returns it as a pandas DataFrame.

    Parameters:
    table_name (str): The name of the table to retrieve data from.

    Returns:
    DataFrame: A pandas DataFrame containing the table data. None if an exception occurs.
    """
    try:
        conn = sqlite3.connect("data_analytics.db")
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)

        return df
    except Exception as e:
        logging.exception(f"Error retrieving data from {table_name}: {e}")
        return None
