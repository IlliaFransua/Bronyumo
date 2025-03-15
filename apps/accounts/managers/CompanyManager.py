import psycopg2

from apps.accounts.DatabaseConnection import DatabaseConnection


class CompanyManager:
    def __init__(self, db_dsn: str):
        """
        Initializes the database connection for the company management service.

        :param db_dsn: The database connection string (Data Source Name).
        """
        self.db_dsn = db_dsn

    def get_company_by_email(self, email: str) -> dict or None:
        """
        Retrieves company details based on the provided email address.

        This method queries the 'companies' table to find a company by its unique email.
        If found, it returns the company details as a dictionary.

        :param email: The email address of the company.
        :return: A dictionary containing company details or None if not found.
        """
        # print(f"Searching for company with email: {email}")
        query = "SELECT * FROM companies WHERE email = %s;"
        try:
            with DatabaseConnection(self.db_dsn) as cursor:
                # print(f"Executing query: {query} with email={email}")
                cursor.execute(query, (email,))
                company = cursor.fetchone()

                if company:
                    # print(f"Company found: {company}")

                    if isinstance(company, dict):
                        company_data = {
                            "id": company.get("id"),
                            "name": company.get("name"),
                            "location": company.get("location"),
                            "email": company.get("email"),
                            "hashed_password": company.get("hashed_password")
                        }
                        # print(f"Converted company data: {company_data}")
                        return company_data
                    else:
                        # print("Company data is not in expected format (dict).")
                        return None
                else:
                    # print("No company found with the provided email.")
                    return None
        except psycopg2.Error as e:
            # print(f"Error retrieving company by email: {e}")
            return None

    def get_company_by_session_id(self, session_id: str) -> dict or None:
        """
        Retrieves company details based on a given session ID.

        This method first looks up the company ID associated with the session ID
        in the 'company_sessions' table. If found, it then fetches the corresponding
        company details from the 'companies' table.

        :param session_id: The unique identifier of the session.
        :return: A dictionary containing company details or None if not found.
        """
        # print(f"Searching for company with session ID: {session_id}")

        session_query = "SELECT company_id FROM company_sessions WHERE session_id = %s;"
        try:
            with DatabaseConnection(self.db_dsn) as cursor:
                # print(f"Executing query: {session_query} with session_id={session_id}")
                cursor.execute(session_query, (session_id,))
                session = cursor.fetchone()

                if session:
                    company_id = session.get("company_id")
                    if company_id is not None:
                        # print(f"Company ID retrieved: {company_id}")

                        company_query = "SELECT * FROM companies WHERE id = %s;"
                        cursor.execute(company_query, (company_id,))
                        company = cursor.fetchone()

                        if company:
                            # print(f"Company found: {company}")

                            if isinstance(company, dict):
                                company_data = {
                                    "id": company.get("id"),
                                    "name": company.get("name"),
                                    "location": company.get("location"),
                                    "email": company.get("email"),
                                    "hashed_password": company.get("hashed_password")
                                }
                                # print(f"Converted company data: {company_data}")
                                return company_data
                            else:
                                # print("Company data is not in expected format (dict).")
                                return None
                        else:
                            # print("No company found with the provided company_id.")
                            return None
                    else:
                        # print("No company_id found in session data.")
                        return None
                else:
                    # print("No session found with the provided session ID.")
                    return None
        except psycopg2.Error as e:
            # print(f"Error retrieving company by session_id: {e}")
            return None

    def get_company_by_id(self, company_id: int) -> dict or None:
        """
        Retrieves company details from the database using the company ID.

        :param company_id: The unique identifier of the company.
        :return: A dictionary containing company details or None if not found.
        """
        query = "SELECT * FROM companies WHERE company_id = %s;"
        try:
            with DatabaseConnection(self.db_dsn) as cursor:
                # print(f"Executing query: {query} with company_id={company_id}")
                cursor.execute(query, (company_id,))
                company = cursor.fetchone()

                if company:
                    # print(f"Company found: {company}")

                    if isinstance(company, dict):
                        company_data = {
                            "id": company.get("company_id"),
                            "name": company.get("name"),
                            "location": company.get("location"),
                            "email": company.get("email"),
                            "hashed_password": company.get("hashed_password")
                        }
                        # print(f"Converted company data: {company_data}")
                        return company_data
                    else:
                        # print("Company data is not in expected format (dict).")
                        return None
                else:
                    # print("No company found with the provided company_id.")
                    return None
        except psycopg2.Error as e:
            # print(f"Error retrieving company by company_id: {e}")
            return None

    def create_company(self, name: str, location: str, email: str, hashed_password: str) -> int or None:
        """
        Creates a new company in the database and returns its unique ID.

        :param name: The name of the company.
        :param location: The location of the company.
        :param email: The email address of the company.
        :param hashed_password: The hashed password for authentication.
        :return: The ID of the newly created company or None if creation fails.
        """
        query = """
        INSERT INTO companies (name, location, email, hashed_password)
        VALUES (%s, %s, %s, %s)
        RETURNING id;
        """

        try:
            with psycopg2.connect(self.db_dsn) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (name, location, email, hashed_password))
                    company_id = cursor.fetchone()  # (8,) or None

                    if company_id:
                        return int(company_id[0])
                    else:
                        # print("Error: INSERT request did not return ID.")
                        return None
        except psycopg2.IntegrityError:
            # print(f"Error: Company with email {email} already exists.")
            return None
        except psycopg2.Error as e:
            # print(f"Database error: {e}")
            return None

    def get_company(self, company_id: int) -> dict or None:
        """
        Retrieves company details from the database by its unique ID.

        :param company_id: The unique identifier of the company.
        :return: A dictionary containing company details or None if not found.
        """
        query = "SELECT * FROM companies WHERE id = %s;"
        try:
            with DatabaseConnection(self.db_dsn) as cursor:
                cursor.execute(query, (company_id,))
                return cursor.fetchone()
        except psycopg2.Error as e:
            # print(f"Error retrieving company: {e}")
            return None

    def update_company(self, company_id: int, name: str = None, location: str = None, email: str = None,
                       hashed_password: str = None) -> bool:
        """
        Updates company information in the database.

        :param company_id: The unique identifier of the company.
        :param name: (Optional) The new name of the company.
        :param location: (Optional) The new location of the company.
        :param email: (Optional) The new email address of the company.
        :param hashed_password: (Optional) The new hashed password.
        :return: True if the update was successful, False otherwise.
        """
        fields = []
        values = []

        if name:
            fields.append("name = %s")
            values.append(name)
        if location:
            fields.append("location = %s")
            values.append(location)
        if email:
            fields.append("email = %s")
            values.append(email)
        if hashed_password:
            fields.append("hashed_password = %s")
            values.append(hashed_password)

        if not fields:
            return False

        query = f"UPDATE companies SET {', '.join(fields)} WHERE id = %s;"
        values.append(company_id)

        try:
            with DatabaseConnection(self.db_dsn) as cursor:
                cursor.execute(query, values)
                return cursor.rowcount > 0
        except psycopg2.Error as e:
            # print(f"Error updating company: {e}")
            return False

    def delete_company(self, company_id: int) -> bool:
        """
        Deletes a company from the database by its ID.

        :param company_id: The unique identifier of the company to be deleted.
        :return: True if the company was successfully deleted, False otherwise.
        """
        query = "DELETE FROM companies WHERE id = %s;"
        try:
            with DatabaseConnection(self.db_dsn) as cursor:
                cursor.execute(query, (company_id,))
                return cursor.rowcount > 0
        except psycopg2.Error as e:
            # print(f"Error deleting company: {e}")
            return False

    def company_exists(self, email: str) -> bool:
        """
        Checks whether a company with the given email exists in the database.

        :param email: The email address of the company to check.
        :return: True if the company exists, False otherwise.
        """
        query = "SELECT 1 FROM companies WHERE email = %s;"
        try:
            with DatabaseConnection(self.db_dsn) as cursor:
                cursor.execute(query, (email,))
                return cursor.fetchone() is not None
        except psycopg2.Error as e:
            # print(f"Error checking if company exists: {e}")
            return False
