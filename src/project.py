import pandas as pd
import psycopg2
import streamlit as st
from configparser import ConfigParser

@st.cache
def get_config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)
    return {k: v for k, v in parser.items(section)}


@st.cache
def query_db(sql: str):
    # print(f'Running query_db(): {sql}')

    db_info = get_config()

    # Connect to an existing database
    connection = psycopg2.connect(**db_info)

    # Open a cursor to perform database operations
    cursor = connection.cursor()

    # Execute a command: this creates a new table
    cursor.execute(sql)

    # Obtain data
    data = cursor.fetchall()

    column_names = [desc[0] for desc in cursor.description]

    # Make the changes to the database persistent
    connection.commit()

    # Close communication with the database
    cursor.close()
    connection.close()

    df = pd.DataFrame(data=data, columns=column_names)

    return df