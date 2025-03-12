import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Optional, Any

class DatabaseConnection:
    def __init__(self, dsn: str):
        """
        Initializes the object for interacting with the database.

        This method stores the connection string (DSN) for later use when connecting
        to the database and creates objects for the connection and cursor.

        :param dsn: The Data Source Name (DSN) containing all necessary information
                     to connect to the database.
        """
        self.dsn = dsn
        self.conn: Optional[psycopg2.extensions.connection] = None
        self.cursor: Optional[RealDictCursor] = None

    def __enter__(self) -> RealDictCursor:
        """
        Opens a connection to the database and creates a cursor.

        This method is called when using the `with` statement, opening a connection
        to the database, creating a cursor, and returning it for query execution.

        :return: The cursor for executing SQL queries and returning data as dictionaries.
        :raises: psycopg2.Error if the connection to the database could not be established.
        """
        try:
            self.conn = psycopg2.connect(self.dsn)
            self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            return self.cursor
        except psycopg2.Error as e:
            # print(f"Error connecting to the database: {e}")
            raise

    def __exit__(self, exc_type: Optional[type], exc_val: Optional[Exception], exc_tb: Optional[Any]) -> None:
        """
        Closes the connection and cursor after the block of code using `with` has executed.

        This method is called after executing the query (or in case of an exception),
        performing either a rollback or commit, then closing the cursor and connection.

        :param exc_type: The type of exception, if one occurred in the `with` block.
        :param exc_val: The exception message, if an exception occurred.
        :param exc_tb: The traceback of the exception, if one occurred.
        """
        if self.cursor:
            if exc_type is not None:
                self.conn.rollback()
                # print(f"Transaction rolled back due to: {exc_val}")
            else:
                self.conn.commit()
            self.cursor.close()
        if self.conn:
            self.conn.close()
