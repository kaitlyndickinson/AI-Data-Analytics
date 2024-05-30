# Prompts for the OpenAI model. Can modify or add new System prompt here.

def sql_prompt(question, schema):
    """
    Generates a prompt for creating a syntactically correct SQLite query based on the user's question and table schema.

    Parameters:
    question (str): The user's question that needs to be answered with an SQL query.
    schema (str): The schema of the table(s) involved in the SQL query.

    Returns:
    str: The generated prompt for creating the SQL query.
    """
    prompt = f"""Given the user's question and the below table schema, create a syntactically correct SQLite query to run.
                Unless the user specifies in the question a specific number of examples to obtain, query for at most 5 results using the LIMIT clause as per SQLite. 
                You can order the results to return the most informative data in the database. Never query for all columns from a table. 
                You must query only the columns that are needed to answer the question. ONLY output the SQL query with no additional text.
                The output will be used to directly query a SQLite database.

                Question: {question}

                Table Schema:
                {schema}
                """
    
    return prompt


def qa_prompt(question, query, response):
    """
    Generates a prompt for answering a question based on an SQL query and its response.

    Parameters:
    question (str): The user's question that the SQL query is intended to answer.
    query (str): The SQL query that was executed to retrieve the response.
    response (str): The result obtained from executing the SQL query.

    Returns:
    str: The generated prompt for answering the user's question based on the SQL query and response.
    """
    prompt = f"""Given the SQL query and the response of the SQL query, answer the question below.
    
    Query: {query}

    Result: {response}

    User's Question: {question}
    """

    return prompt
