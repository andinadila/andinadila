import streamlit as st
from multiApp import Multipage

import sys
sys.path.append("./apps")
from apps import home, searchEntry, uploadFile, history
import psycopg2
from configuration import config

app = Multipage()

app.add_page("Home", home.app)
app.add_page("Search Entry", searchEntry.app)
app.add_page("Upload File", uploadFile.app)
app.add_page("History", history.app)

app.run()

def connect():
    #not return anything basically it plays the role of a flag somehow
    connection = None
    try:
        params = config()
        print('Connecting to the postgreSQL database...')
        connection = psycopg2.connect(**params) #we want to extract everything inside the params inside those two parentheses and to connect using the psycopg2 module

        #create a cursor
        crsr = connection.cursor()
        print('PostgreSQL database version: ')
        crsr.execute('SELECT version()')
        db_version = crsr.fetchone()
        print(db_version)
        #close the cursor, because the cursor and the connection is the communication way between the py file and the db
        crsr.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()
            print('Database connection terminated.')

if __name__ == "__main__":
    connect()

