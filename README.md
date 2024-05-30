# AI Data Analytics Tool

## Purpose
This AI Data Analytics Tool allows you to upload a CSV file (or excel sheet), and automatically parse and store the data in a SQLite database so you can chat over your data with an AI.

### Features
- Upload and delete datasets.
- Automatically parse, determine data types for columns, determine column names, determine table name, and store data in a SQLite database.
- Navigate across multiple chat threads.
- Easy access "View Data" button so you don't need to go back to the original copy.


### What This Tool Does
- Allows you to upload and manage SQLite databases that are created by uploading CSV files.
- Automatically parses through your CSV data and creates a SQLite table in a database called data_analytics.db.
- Automatically determins the data types and column names of the data when creating the table.
- Allows you to create and navigate different chat threads.
- Allows you to **switch** between tables in a singular chat thread, **one at a time**.
- Stores structured data in a SQLite database and uses an OpenAI model to construct a syntactically correct query, then the results are ran and passed in another API call to generate a final answer.

### What This Tool Doesn't Do
- Utilize multiple datasets in one question.
- Automatically determined which datasets to use.
- Uses a Vectorstore (AKA RAG) *I have another full-fledged rag based application I plan to publish soon, though.*

### "Why should I use this?"
I've seen similar tools, but I haven't came across one where you don't need to automatically define the structure of your data. This AI tool allows you to simply upload your CSV file and it will determine the structure of the SQL schema for you, so you don't need to worry about manually inputting everything.

### Additional Information
- There is a "app_logger.log" file that logs the SQL query the model comes up with and it's response. I find these pretty interesting to look at, it comes up with some neat queries and can answer pretty complex questions. If you encounter any errors, this is also where you want to look.
- You can change the model being used in the llm.py file, simply kept it on gpt-3.5-turbo since it's cheap.
- If you come across this repository and have any feature requests, feel free to open an issue! Also, if you want to collaborate, feel free to mess around and open a pull request!

## Future Plans
- Ability to automatically determine which datasets to pull from and construct multiple queries at once (would be useful for comparing data across multiple datasets).
- Generate diagrams, documents, and findings in one singular document (could be useful for companies wanting a automatic way to quickly analyze data without manually going through the CSV files).
- In general, better error handling. This was a quick prototype I whipped up so there may be issues I haven't handled yet.