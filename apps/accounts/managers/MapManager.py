import psycopg2

from apps.accounts.DatabaseConnection import DatabaseConnection


class MapManager:
    def __init__(self, db_dsn: str):
        """
        Initializes the database connection for the company-map management service.

        :param db_dsn: The database connection string (Data Source Name).
        """
        self.db_dsn = db_dsn

    def get_first_map_hash_by_company_id(self, company_id: int) -> str or None:
        """
        Retrieves the first map_hash associated with the given company ID.

        :param company_id: The unique identifier of the company.
        :return: The first associated map_hash as a string or None if not found.
        """
        query = """
                SELECT cm.map_hash 
                FROM company_map cm
                WHERE cm.company_id = %s
                ORDER BY cm.map_hash ASC
                LIMIT 1;
                """
        try:
            with DatabaseConnection(self.db_dsn) as cursor:
                cursor.execute(query, (company_id,))
                result = cursor.fetchone()

                if result:
                    return result["map_hash"]
                else:
                    return None
        except psycopg2.DatabaseError as e:
            raise e
        except psycopg2.InterfaceError as e:
            raise e
        except Exception as e:
            raise e
