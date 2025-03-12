from apps.accounts.DatabaseConnection import DatabaseConnection
from datetime import datetime, timedelta
import uuid
import psycopg2
import pytz
import threading
import time

class CompanySessionManager:
    def __init__(self, db_dsn):
        """
        Initializes the database connection settings.

        This constructor stores the database connection string (DSN) for future interactions
        with the database.

        :param db_dsn: The Data Source Name (DSN) for connecting to the database.
        """
        self.db_dsn = db_dsn
        self.start_session_cleanup(interval=3600)

    def start_session(self, company_id, expires_in=3600):
        """
        Starts a new session for a given company.

        This method generates a new session ID, sets its expiration time, and inserts the session
        into the 'company_sessions' table.

        :param company_id: The ID of the company for which the session is being created.
        :param expires_in: The session duration in seconds (default is 3600 seconds, or 1 hour).
        :return: A tuple containing the session ID and expiration timestamp, or None if the session could not be created.
        """
        session_id = uuid.uuid4()
        expires_at = datetime.utcnow() + timedelta(seconds=expires_in)

        query = """
        INSERT INTO company_sessions (session_id, company_id, created_at, expires_at)
        VALUES (%s, %s, CURRENT_TIMESTAMP, %s)
        RETURNING session_id;
        """

        try:
            with psycopg2.connect(self.db_dsn) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (session_id, company_id, expires_at))
                    result = cursor.fetchone()  # (UUID,) or None

                    if result is None:
                        # print(f"Error: INSERT query did not return session_id for company_id={company_id}")
                        return None

                    return result[0], expires_at

        except psycopg2.IntegrityError:
            # print(f"Error: Integrity violation when creating session for company_id={company_id}")
            return None
        except psycopg2.Error as e:
            # print(f"Database error while creating session: {e}")
            return None

    def validate_session(self, session_id):
        """
        Validates whether a given session is active and not expired.

        This method checks if a session with the provided session ID exists in the 'company_sessions' table
        and ensures that its expiration time has not yet passed.

        :param session_id: The unique identifier of the session to validate.
        :return: True if the session is valid and not expired, False otherwise.
        """
        query = "SELECT * FROM company_sessions WHERE session_id = %s;"
        try:
            with DatabaseConnection(self.db_dsn) as cursor:
                cursor.execute(query, (session_id,))
                session = cursor.fetchone()

                # print(f"Session data retrieved: {session}")
                # print(f"Session structure: {session}")
                # print(f"Available session keys: {session.keys()}")

                if session:
                    expires_at = session['expires_at'].astimezone(pytz.UTC)
                    current_time = datetime.utcnow().replace(tzinfo=pytz.UTC)

                    # print(f"Session expires at: {expires_at}")
                    # print(f"Current time: {current_time}")

                    return expires_at > current_time

                return False
        except psycopg2.Error as e:
            # print(f"Error validating session: {e}")
            return False

    def end_session(self, session_id):
        """
        Ends a company session by deleting it from the 'company_sessions' table.

        This method removes a session associated with the given session ID, effectively logging out the company.

        :param session_id: The unique identifier of the session to be ended.
        :return: True if the session was successfully deleted, False otherwise.
        """
        query = "DELETE FROM company_sessions WHERE session_id = %s;"
        try:
            with DatabaseConnection(self.db_dsn) as cursor:
                cursor.execute(query, (session_id,))
                return cursor.rowcount > 0
        except psycopg2.Error as e:
            # print(f"Error ending session: {e}")
            return False

    def clean_expired_sessions(self):
        """
        Removes expired company sessions from the 'company_sessions' table.

        This method deletes all sessions where the expiration time has passed, ensuring session data remains up to date.

        :return: The number of expired sessions that were deleted.
        """
        query = "DELETE FROM company_sessions WHERE expires_at < CURRENT_TIMESTAMP;"
        try:
            with DatabaseConnection(self.db_dsn) as cursor:
                cursor.execute(query)
                return cursor.rowcount
        except psycopg2.Error as e:
            # print(f"Error cleaning expired sessions: {e}")
            return 0

    def start_session_cleanup(self, interval=3600):
        """
        Starts a background thread that periodically cleans up expired sessions.

        :param interval: The interval (in seconds) between each cleanup. Default is 3600 seconds (1 hour).
        """
        def cleanup_task():
            while True:
                self.clean_expired_sessions()
                time.sleep(interval)

        cleanup_thread = threading.Thread(target=cleanup_task)
        cleanup_thread.daemon = True
        cleanup_thread.start()

    def refresh_session(self, session_id: str, expires_in: int = 3600) -> bool:
        """
        Extends the expiration time of an existing session.

        This method updates the 'expires_at' field of a session, effectively extending its validity.

        :param session_id: The ID of the session to be refreshed.
        :param expires_in: The additional duration (in seconds) to extend the session.
        :return: True if the session was successfully updated, False otherwise.
        """
        new_expires_at = datetime.utcnow() + timedelta(seconds=expires_in)

        query = "UPDATE company_sessions SET expires_at = %s WHERE session_id = %s;"

        try:
            with DatabaseConnection(self.db_dsn) as cursor:
                cursor.execute(query, (new_expires_at, session_id))
                return cursor.rowcount > 0
        except psycopg2.Error as e:
            # print(f"Error refreshing session: {e}")
            return False
