import json
from builtins import str, bool
from typing import List, Dict

import psycopg2
from psycopg2.extras import execute_values

from apps.accounts.DatabaseConnection import DatabaseConnection


class MapManager:
    def __init__(self, db_dsn: str):
        """
        Initializes the database connection for the company-map management service.

        :param db_dsn: The database connection string (Data Source Name).
        """
        self.db_dsn = db_dsn

    def check_booking_object_belongs_to_map(self, map_hash: str, booking_object_hash: str) -> bool:
        """
        Checks if the booking object belongs to the specified map.

        :param map_hash: The hash of the map.
        :param booking_object_hash: The hash of the booking object.
        :return: True if the booking object belongs to the map, otherwise False.
        """
        query = """
        SELECT 1
        FROM booking_objects
        WHERE map_hash = %s AND booking_object_hash = %s;
        """
        try:
            with DatabaseConnection(self.db_dsn) as cursor:
                cursor.execute(query, (map_hash, booking_object_hash))
                result = cursor.fetchone()

            return result is not None
        except Exception as e:
            print(f"An error occurred when checking whether the booking object belongs to the card: {e}")
            raise e

    def save_or_update_booking_objects(self, map_hash: str, booking_objects: List[Dict],
                                       booking_availability: Dict[str, list]) -> List[str]:
        """
        Saves or updates booking objects and removes missing objects.

        :param map_hash: The hash of the map.
        :param booking_objects: A list of booking objects (with hashes and coordinates).
        :param booking_availability: The availability of the objects.
        :return: A list of hashes of updated or created booking objects.
        """
        query = """
        SELECT booking_object_hash FROM booking_objects WHERE map_hash = %s;
        """
        try:
            with DatabaseConnection(self.db_dsn) as cursor:
                cursor.execute(query, (map_hash,))
                current_objects = cursor.fetchall()

            current_object_hashes = {str(obj['booking_object_hash']) for obj in current_objects}
            new_object_hashes = {obj['booking_object_hash'] for obj in booking_objects}

            to_delete = current_object_hashes - new_object_hashes
            if to_delete:
                delete_query = """
                DELETE FROM booking_objects WHERE booking_object_hash IN %s;
                """
                with DatabaseConnection(self.db_dsn) as cursor:
                    cursor.execute(delete_query, (tuple(to_delete),))
                print(f"Removed objects with hash: {to_delete}")

            updated_or_added_hashes = []
            for booking_object in booking_objects:
                booking_object_hash = booking_object['booking_object_hash']
                if str(booking_object_hash) in current_object_hashes:
                    updated_or_added_hashes.append(self.update_booking_object(booking_object, booking_availability))
                else:
                    updated_or_added_hashes.append(
                        self.create_booking_object(map_hash, booking_object, booking_availability))

            return updated_or_added_hashes
        except Exception as e:
            print(f"Error in booking objects processing: {e}")
            raise e

    def update_booking_object_hours(self, booking_object_hash: str, booking_availability: Dict[str, list]) -> str:
        """
        Updates only the booking hours of the object.

        :param booking_object_hash: The hash of the booking object.
        :param booking_availability: The new booking schedule.
        :return: The hash of the updated booking object.
        """
        query = """
        UPDATE booking_objects
        SET booking_availability = %s
        WHERE booking_object_hash = %s
        RETURNING booking_object_hash;
        """
        try:
            with DatabaseConnection(self.db_dsn) as cursor:
                cursor.execute(query, (
                    json.dumps(booking_availability),
                    booking_object_hash
                ))
                result = cursor.fetchone()
                if result:
                    cursor.connection.commit()
                    return str(result['booking_object_hash'])
                else:
                    raise Exception(f"Failed to update hours for the object with hash {booking_object_hash}")
        except Exception as e:
            print(f"Error updating booking object hours: {e}")
            raise e

    def update_all_booking_objects_hours(self, map_hash: str, booking_availability: Dict[str, list]) -> bool:
        """
        Updates booking hours for all objects on the map.

        :param map_hash: The hash of the map.
        :param booking_availability: The new booking schedule.
        :return: True if the update was successful, False otherwise.
        """
        query = """
        UPDATE booking_objects
        SET booking_availability = %s
        WHERE map_hash = %s;
        """
        try:
            with DatabaseConnection(self.db_dsn) as cursor:
                cursor.execute(query, (
                    json.dumps(booking_availability),
                    map_hash
                ))
                cursor.connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating booking hours for all objects: {e}")
            raise e

    import json

    def update_booking_objects(self, map_hash: str, booking_objects: list) -> list:
        """
        Updates multiple booking objects for the given map.

        :param map_hash: The hash of the map.
        :param booking_objects: List of booking objects with their data.
        :return: List of updated booking object hashes.
        """
        print(f"Получает map_hash (type({map_hash})): ", map_hash)
        print(f"Получает booking_objects (type({booking_objects})): ", booking_objects)

        query = """
        UPDATE booking_objects AS bo
        SET x_min = %s,
            x_max = %s,
            y_min = %s,
            y_max = %s,
            booking_availability = %s
        WHERE bo.map_hash = %s AND bo.booking_object_hash = %s
        RETURNING bo.booking_object_hash;
        """

        updated_hashes = []

        try:
            with DatabaseConnection(self.db_dsn) as cursor:
                for obj in booking_objects:
                    # Если нет данных доступности, не обновляем поле booking_availability
                    availability_json = None
                    if 'booking_availability' in obj:
                        availability_json = json.dumps(obj['booking_availability'])

                    # Проверка координат и данных
                    print(f"Обновляем объект: {obj['booking_object_hash']}, координаты: "
                          f"x_min={obj['x_min']}, x_max={obj['x_max']}, y_min={obj['y_min']}, y_max={obj['y_max']}")

                    # Выполнение запроса
                    cursor.execute(query, (
                        obj['x_min'],
                        obj['x_max'],
                        obj['y_min'],
                        obj['y_max'],
                        availability_json if availability_json else None,
                        map_hash,
                        obj['booking_object_hash']
                    ))

                    result = cursor.fetchone()
                    if result:
                        updated_hashes.append(result['booking_object_hash'])
                    else:
                        print(f"Failed to update object hash {obj['booking_object_hash']}")

                print("Updated booking object hashes:", updated_hashes)
                return updated_hashes

        except Exception as e:
            print(f"Error while updating booking objects: {e}")
            raise e

    def create_booking_object(self, map_hash: str, x_min: float, x_max: float, y_min: float, y_max: float,
                              booking_availability: dict) -> str:
        """
        Creates a new booking object.

        :param map_hash: The hash of the map.
        :param x_min, x_max, y_min, y_max: The coordinates of the object.
        :param booking_availability: The availability of the object.
        :return: The hash of the new booking object.
        """
        query = """
        INSERT INTO booking_objects (map_hash, x_min, x_max, y_min, y_max, booking_availability)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING booking_object_hash;
        """
        try:
            with DatabaseConnection(self.db_dsn) as cursor:
                cursor.execute(query, (
                    map_hash,
                    x_min,
                    x_max,
                    y_min,
                    y_max,
                    json.dumps(booking_availability)
                ))
                booking_object_hash = cursor.fetchone()
                if booking_object_hash is None:
                    raise ValueError("Failed to create booking object - request did not return hash.")
                return booking_object_hash.get('booking_object_hash')
        except Exception as e:
            print(f"Error while creating a booking object: {e.__class__.__name__}: {e}")
            raise e

    def delete_booking_object(self, map_hash: str, booking_object_hash: str) -> bool:
        """
        Deletes the booking object by the object hash and map hash.

        :param map_hash: The hash of the map.
        :param booking_object_hash: The hash of the booking object.
        :return: True if the object is deleted, False if the object is not found.
        """
        query = """
        DELETE FROM booking_objects
        WHERE map_hash = %s AND booking_object_hash = %s
        RETURNING booking_object_hash;
        """
        try:
            with DatabaseConnection(self.db_dsn) as cursor:
                cursor.execute(query, (map_hash, booking_object_hash))
                result = cursor.fetchone()

                if result:
                    return True
                else:
                    return False
        except Exception as e:
            raise e

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

    def get_booking_objects_by_map_hash(self, map_hash: str) -> List[Dict]:
        """
        Retrieves all booking objects associated with the given map_hash.

        Parameters:
            map_hash (str): The unique identifier (hash) of the map.

        Returns:
            List[Dict]: A list of dictionaries, each containing details of a booking object.
        """
        # Проверяем существование карты перед выполнением запроса на бронирования
        if not self.check_map_hash_existence(map_hash):
            raise ValueError(f"Map with hash {map_hash} does not exist.")

        query = """
                SELECT booking_object_hash, x_min, x_max, y_min, y_max, booking_availability
                FROM booking_objects
                WHERE map_hash = %s;
        """
        try:
            with DatabaseConnection(self.db_dsn) as cursor:
                cursor.execute(query, (map_hash,))
                results = cursor.fetchall()

                booking_objects = [
                    {
                        "booking_object_hash": str(row["booking_object_hash"]),
                        "x_min": row["x_min"],
                        "x_max": row["x_max"],
                        "y_min": row["y_min"],
                        "y_max": row["y_max"],
                        "booking_availability": row["booking_availability"]
                    }
                    for row in results
                ]

                return booking_objects
        except Exception as e:
            raise e

    def get_map_image_path(self, map_hash: str) -> str or None:
        """
        Retrieves the image_path for the given map_hash.

        Parameters:
            map_hash (str): The unique identifier of the map.

        Returns:
            str or None: The image path as a string, or None if not found.
        """
        query = "SELECT image_path FROM maps WHERE map_hash = %s;"
        try:
            with DatabaseConnection(self.db_dsn) as cursor:
                cursor.execute(query, (map_hash,))
                result = cursor.fetchone()
                return result["image_path"] if result else None
        except Exception:
            raise

    def check_map_hash_existence(self, map_hash: str) -> bool:
        """
        Checks if the provided map_hash exists in the database.

        :param map_hash: The unique identifier of the map.
        :return: True if the map_hash exists, False otherwise.
        """
        query = """
                SELECT EXISTS (
                    SELECT 1
                    FROM maps
                    WHERE map_hash = %s
                );
        """
        try:
            with DatabaseConnection(self.db_dsn) as cursor:
                cursor.execute(query, (map_hash,))
                result = cursor.fetchone()

                if result:
                    return result["exists"]
                else:
                    return False
        except psycopg2.DatabaseError as e:
            raise e
        except psycopg2.InterfaceError as e:
            raise e
        except Exception as e:
            raise e

    def map_belongs_to_company(self, map_hash: str, company_id: int) -> bool:
        """
        Checks whether the given map_hash belongs to the specified company.

        Parameters:
            map_hash (str): The unique identifier (hash) of the map.
            company_id (int): The unique identifier of the company.

        Returns:
            bool: True if the map_hash is associated with the company, otherwise False.
        """
        query = """
                SELECT 1
                FROM company_map
                WHERE map_hash = %s AND company_id = %s
                LIMIT 1;
                """
        try:
            with DatabaseConnection(self.db_dsn) as cursor:
                cursor.execute(query, (map_hash, company_id))
                result = cursor.fetchone()
                return bool(result)
        except Exception:
            raise
