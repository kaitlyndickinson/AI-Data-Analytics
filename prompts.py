
def sql_prompt(question, schema):
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
    prompt = f"""Given the SQL query and the responsef the SQL query, answer the question below.
    
    Query: {query}

    Result: {response}

    User's Question: {question}
    """

    return prompt