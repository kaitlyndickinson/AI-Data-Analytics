import sqlite3
import re

def get_dtype(dtype):
    if dtype == "Int64" or dtype == "int64":
        return "INTEGER"
    elif dtype == "Float64" or dtype == "float64":
        return "REAL"
    elif dtype == "boolean":
        return "BOOLEAN"
    else:
        return "TEXT"


def sanitize_column_name(name):
    return re.sub(r"\W+", "", name)


def insert_data(data, table_name):
    conn = sqlite3.connect("data_analytics.db")
    cursor = conn.cursor()

    data_types = data.dtypes.apply(lambda x: x.name).to_dict()

    columns = [
        (
            f"`{sanitize_column_name(col)}` {get_dtype(data_types[col])}"
            if "(" in col
            else f"{sanitize_column_name(col).replace('Group', '`Group`')} {get_dtype(data_types[col])}"
        )
        for col in data.columns
    ]

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
