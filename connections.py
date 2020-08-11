import os
import psycopg2
from psycopg2.pool import SimpleConnectionPool
from dotenv import load_dotenv
from contextlib import contextmanager

load_dotenv()

database_uri = os.environ.get("DATABASE_URI")


def create_connection():
    return psycopg2.connect(database_uri)


connection_pool = SimpleConnectionPool(minconn=1, maxconn=10, dsn=database_uri)


@contextmanager
def get_cursor():
    connection = connection_pool.getconn()
    try:
        yield connection
    finally:
        connection_pool.putconn(connection)
