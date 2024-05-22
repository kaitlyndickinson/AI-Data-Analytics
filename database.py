import sqlite3
import re
import logging

def get_dtype(dtype):
    if dtype == "Int64" or dtype == "int64":
        return "INTEGER"
    elif dtype == "Float64" or dtype == "float64":
        return "REAL"
    elif dtype == "boolean":
        return "BOOLEAN"
    else:
        return "TEXT"


def sanitize(name):
    return re.sub(r"\W+", "", name)


def insert_data(data, table_name):
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
    print(create_table_query)
    cursor.execute(create_table_query)

    for row in data.itertuples(index=False, name=None):
        placeholders = ", ".join(["?" for _ in row])
        insert_query = f"INSERT INTO {table_name} VALUES ({placeholders});"
        cursor.execute(insert_query, row)

    conn.commit()
    conn.close()


def get_tables():
    conn = sqlite3.connect("data_analytics.db")
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    table_names = [table[0] for table in tables]
    return table_names


def get_table(table_name):
    conn = sqlite3.connect("data_analytics.db")
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM {table_name};")
    data = cursor.fetchall()

    conn.close()
    return data

def run_sql_query(query):
    conn = sqlite3.connect("data_analytics.db")
    cursor = conn.cursor()

    try:
        cursor.execute(query)
        data = cursor.fetchall()

        conn.close()
    except Exception as e:
        logging.info(f"Error executing query: {query}, {e}")
    return data
   
def get_table_schema(table_name):
    conn = sqlite3.connect("data_analytics.db")
    cursor = conn.cursor()

    cursor.execute(f"PRAGMA table_info({table_name});")

    schema = cursor.fetchall()
    formatted_schema = format_table_scheme(schema, table_name)

    conn.close()
    return formatted_schema

def format_table_scheme(schema, table_name):
    formatted_schema = f"Table name: {table_name}\n"

    for column in schema:
        formatted_schema += f"Column Name: {column[1]}\n"
        formatted_schema += f"Data Type: {column[2]}\n"
        formatted_schema += f"Not Null: {'Yes' if column[3] else 'No'}\n"
        formatted_schema += f"Default Value: {column[4]}\n"
        formatted_schema += f"Primary Key: {'Yes' if column[5] else 'No'}\n\n"

    return formatted_schema
