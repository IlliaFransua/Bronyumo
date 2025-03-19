import psycopg2

from apps.accounts.DatabaseConnection import DatabaseConnection

class BookingManager():
    def __init__(self, db_dsn: str):
        """
        Initializes the database connection for the company-map management service.

        :param db_dsn: The database connection string (Data Source Name).
        """
        self.db_dsn = db_dsn
    
    def get_list_of_bookings_by_hash(self,map_hash: str) -> list:
        query = """
SELECT br.first_name || ' ' || br.last_name as full_name, br.email, 
		(br.booking_period->>'from')::timestamp::date as "date",
		(br.booking_period->>'from')::timestamp::time as "from",
		(br.booking_period->>'to')::timestamp::time as "to",
		br.booking_object_hash
FROM booking_objects
JOIN booking_records as br on booking_objects.booking_object_hash = br.booking_object_hash

where booking_objects.map_hash = %s
"""
        try:
            with DatabaseConnection(self.db_dsn) as cursor:
                cursor.execute(query, (map_hash,))
                result = cursor.fetchall()
            if result:
                bookings = []
                for booking in result:
                    booking_data = {
                        "booking_object_hash": booking.get("booking_object_hash"),
                        "full_name": booking.get("full_name"),
                        "email": booking.get("email"),
                        "date": booking.get("date"),
                        "start_time": booking.get("from"),
                        "end_time": booking.get("to")
                    }
                    bookings.append(booking_data)
                return bookings
            else:
                return None
        except psycopg2.DatabaseError as e:
            raise e
        except psycopg2.InterfaceError as e:
            raise e
        except Exception as e:
            raise e