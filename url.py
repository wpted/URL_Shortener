from configparser import ConfigParser
import sqlite3
import os  # For path checking
from typing import Union  # For Type Hints

config = ConfigParser()
config.read('config.ini')
DB_PATH = config["DATABASE"]["DB"]


def initialize_database() -> None:
    """
        Check if database exists. If so, read table, else, create database and table.
        :return None
    """
    if os.path.exists(DB_PATH):
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        query = "SELECT url FROM sqlite_master where type='table' AND name='urls';"
        cursor.execute(query)

        if cursor.fetchone() is None:  # If URLs table doesn't exist, creates it
            create_query = "CREATE TABLE urls (id PRIMARY KEY, url TEXT);"
            cursor.execute(create_query)
            connection.commit()

        connection.close()

    else:
        # Create Database and URLs table
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        create_query = "CREATE TABLE urls (id PRIMARY KEY, url TEXT);"
        cursor.execute(create_query)
        connection.commit()
        connection.close()


def get_url(id: int) -> Union[str, None]:
    """
       Fetching the Long Url by its ID.
       :return str or None
    """
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    query = "SELECT url FROM urls WHERE id=(?);"
    cursor.execute(query, (id,))
    data = cursor.fetchone()  # Returns the row of the query result [url], None if nothing query result is nothing

    if data:
        return data[0]  # Returns the found url if data is not None
    return None


def url_exists(url: str) -> bool:
    """
    Check whether if the inserted url exists.
    :param url: str
    :return: bool
    """
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    query = "SELECT url FROM urls where url=(?);"
    data = cursor.execute(query, (url,))
    connection.close()
    if data:
        return True
    return False


def insert_url(url: str) -> int:
    """
    Stores the input url into the database and returns the id.
    :param url: str
    :return: int
    """
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    insert_query = "INSERT INTO urls VALUES url=(?);"
    cursor.execute(insert_query, (url,))
    return cursor.lastrowid  # Retrieve inserted id after inserting row
