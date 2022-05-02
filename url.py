from configparser import ConfigParser
import sqlite3
import os  # For path checking
from typing import Union  # For Type Hints

configparser = ConfigParser()
config.read('config.ini')
DB_PATH = config["DATABASE"]["DB"]


def initialize_database() -> None:
    """
    Check if database exists. If so, read table, else, create database and table.
    """
    if os.path.exists(DB_PATH):
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        query = "SELECT url FROM sqlite_master where type='table' AND name='urls'"
        cursor.execute(query)

        if cursor.fetchone() is None:  # If URLs table doesn't exist, create it
            create_query = "CREATE TABLE urls (id PRIMARY KEY, url TEXT)"
            cursor.execute(create_query)
            connection.commit()

        connection.close()


    else:  # Create Database and URLs table
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        create_query = "CREATE TABLE urls (id PRIMARY KEY, url TEXT)"
        cursor.execute(create_query)
        connection.commit()
        connection.close()
