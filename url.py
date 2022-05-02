from configparser import ConfigParser
import sqlite3
import os  # For path checking
from typing import Union  # For Type Hints
from urllib.parse import urlparse

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
        query = "SELECT name FROM sqlite_master where type='table' AND name='urls';"
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
        create_query = "CREATE TABLE urls (id INTEGER PRIMARY KEY, url TEXT);"
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
    if data.fetchone() is not None:
        connection.close()
        return True
    connection.close()
    return False


def insert_url(url: str) -> int:
    """
    Stores the input url into the database and returns the id.
    :param url: str
    :return: int
    """
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    insert_query = "INSERT INTO urls (url) VALUES (?)"
    cursor.execute(insert_query, (url,))
    connection.commit()
    connection.close()

    return cursor.lastrowid  # Retrieve inserted id after inserting row


def get_url_id(url: str) -> int:
    """
    Return the integer id corresponding to the provided long url
    :param url: str
    :return: int
    """
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    query = "SELECT id FROM urls WHERE url=(?)"
    data = cursor.execute(query, (url,)).fetchone()[0]  # [id]
    connection.close()
    return data  # Retrieve id for the input url


def base_url(url: str) -> str:
    """
    For the input long url, return the base url.
    :param url: str
    :return: str
    """
    parse_result = urlparse(url)
    return f"{parse_result.scheme}://{parse_result.hostname}"


def short_url(url: str) -> str:
    """
    For the input long url, return the requested shorten url.
    :param url: str
    :return: str
    """
    base = base_url(url)
    if url_exists(url):
        id = get_url_id(url)
    else:
        id = insert_url(url)

    print(id)

    return f"{base}?id={str(id)}"


def main():
    test_url = "https://www.google.com/search?gs_ssp=eJzj4tLP1TcwMs8rzzYyYPRiycvMSwQALygFIA&q=nina&rlz=1C5CHFA_enTW994TW994&oq=nina&aqs=chrome.1.69i57j46i39j46i67j46i175i199i512l2j0i512j46i512l2j46i175i199i512j46i512.6943j0j1&sourceid=chrome&ie=UTF-8"
    initialize_database()

    shorten_url = short_url(test_url)
    print(f"{test_url=}")
    print(f"{shorten_url=}")

    test_url_2 = "https://www.google.com/search?q=%E6%A5%8A%E7%B4%AB&rlz=1C5CHFA_enTW994TW994&oq=%E6%A5%8A%E7%B4%AB&aqs=chrome..69i57j46i512j46i131i433i512j0i131i433i512l2j69i60l2j69i61.13659j1j9&sourceid=chrome&ie=UTF-8"
    shorten_url_2 = short_url(test_url_2)
    print(f"{test_url_2=}")
    print(f"{shorten_url_2=}")

    test_url_3 = "https://www.google.com/search?q=%E6%A5%8A%E7%B4%AB&rlz=1C5CHFA_enTW994TW994&oq=%E6%A5%8A%E7%B4%AB&aqs=chrome..69i57j46i512j46i131i433i512j0i131i433i512l2j69i60l2j69i61.13659j1j9&sourceid=chrome&ie=UTF-8"
    shorten_url_3 = short_url(test_url_2)
    print(f"{test_url_3=}")
    print(f"{shorten_url_3=}")




if __name__ == "__main__":
    main()
