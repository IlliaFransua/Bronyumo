import json
from typing import List, Dict

import psycopg2
from apps.accounts.DatabaseConnection import DatabaseConnection


class MapManager:
    def __init__(self, db_dsn: str):
        """
        Initializes the database connection for the company-map management service.

        :param db_dsn: The database connection string (Data Source Name).
        """
        self.db_dsn = db_dsn

    def save_or_update_booking_objects(self, map_hash: str, booking_objects: List[Dict],
                                       booking_availability: Dict[str, list]) -> List[str]:
        """
        Сохраняет или обновляет объекты бронирования и удаляет отсутствующие объекты.

        :param map_hash: Хеш карты.
        :param booking_objects: Список объектов бронирования (с хешами и координатами).
        :param booking_availability: Доступность объектов.
        :return: Список хешей обновленных или созданных объектов бронирования.
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
                print(f"Удалены объекты с хешами: {to_delete}")

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
            print(f"Ошибка при обработке объектов бронирования: {e}")
            raise e

    def update_booking_object(self, booking_object: Dict, booking_availability: Dict[str, list]) -> str:
        """
        Обновляет объект бронирования.

        :param booking_object: Объект бронирования с его данными.
        :param booking_availability: Доступность объекта.
        :return: Хеш обновленного объекта бронирования.
        """
        query = """
        UPDATE booking_objects
        SET x_min = %s, x_max = %s, y_min = %s, y_max = %s, booking_availability = %s
        WHERE booking_object_hash = %s
        RETURNING booking_object_hash;
        """
        try:
            with DatabaseConnection(self.db_dsn) as cursor:
                cursor.execute(query, (
                    booking_object['x_min'],
                    booking_object['x_max'],
                    booking_object['y_min'],
                    booking_object['y_max'],
                    json.dumps(booking_availability),
                    booking_object['booking_object_hash']
                ))
                result = cursor.fetchone()
                if result:
                    return str(result['booking_object_hash'])
                else:
                    raise Exception(f"Не удалось обновить объект с хешом {booking_object['booking_object_hash']}")
        except Exception as e:
            print(f"Ошибка при обновлении объекта бронирования: {e}")
            raise e

    def update_booking_objects(self, map_hash: str, new_objects: List[Dict]) -> None:
        """
        Обновляет объекты бронирования для указанной карты:
        - Удаляет объекты, которые не входят в новый список.
        - Обновляет координаты существующих объектов.
        - Добавляет новые объекты.

        :param map_hash: Хеш карты.
        :param new_objects: Новый список объектов с координатами и хешами.
        """
        try:
            existing_objects = self.get_booking_objects_by_map_hash(map_hash)

            new_objects_dict = {obj['booking_object_hash']: obj for obj in new_objects}
            existing_objects_dict = {obj['booking_object_hash']: obj for obj in existing_objects}

            # 1. Удаляет объекты, которые не входят в новый список
            for booking_object_hash, existing_obj in existing_objects_dict.items():
                if booking_object_hash not in new_objects_dict:
                    self.delete_booking_object(map_hash, booking_object_hash)
                    print(f"Объект {booking_object_hash} был удален.")

            # 2. Обновляем существующие объекты (координаты и доступность)
            for booking_object_hash, new_obj in new_objects_dict.items():
                if booking_object_hash in existing_objects_dict:
                    # Обновляет координаты существующих объектов
                    existing_obj = existing_objects_dict[booking_object_hash]
                    if (existing_obj["x_min"] != new_obj["x_min"] or
                            existing_obj["x_max"] != new_obj["x_max"] or
                            existing_obj["y_min"] != new_obj["y_min"] or
                            existing_obj["y_max"] != new_obj["y_max"]):
                        self.update_booking_object(booking_object_hash, new_obj)
                        print(f"Объект {booking_object_hash} был обновлен.")
                else:
                    # Добавляет новые объекты
                    self.create_booking_object(
                        map_hash,
                        new_obj["x_min"],
                        new_obj["x_max"],
                        new_obj["y_min"],
                        new_obj["y_max"],
                        new_obj["booking_availability"]
                    )
                    print(f"Объект {booking_object_hash} был добавлен.")

        except Exception as e:
            print(f"Произошла ошибка при обновлении объектов бронирования: {e}")
            raise e

    def create_booking_object(self, map_hash: str, x_min: float, x_max: float, y_min: float, y_max: float,
                              booking_availability: dict) -> str:
        """
        Создает новый объект бронирования.

        :param map_hash: Хеш карты.
        :param x_min, x_max, y_min, y_max: Координаты объекта.
        :param booking_availability: Доступность объекта.
        :return: Хеш нового объекта бронирования.
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
                    raise ValueError("Не удалось создать объект бронирования — запрос не вернул хеш.")
                return booking_object_hash.get('booking_object_hash')
        except Exception as e:
            print(f"Ошибка при создании объекта бронирования: {e.__class__.__name__}: {e}")
            raise e

    def save_or_update_booking_object(self, map_hash: str, x_min: float, x_max: float, y_min: float, y_max: float,
                                      booking_availability: Dict[str, list]) -> str:
        """
        Сохраняет или обновляет объект бронирования.

        :param map_hash: Хеш карты.
        :param x_min, x_max, y_min, y_max: Координаты объекта.
        :param booking_availability: Доступность объекта.
        :return: Хеш объекта бронирования.
        """
        # Проверяем тип данных для booking_availability
        if not isinstance(booking_availability, dict):
            raise ValueError("booking_availability должен быть словарем.")

        # 1. Попытка обновить объект
        query = """
        UPDATE booking_objects
        SET x_min = %s, x_max = %s, y_min = %s, y_max = %s, booking_availability = %s
        WHERE map_hash = %s
        RETURNING booking_object_hash;
        """
        try:
            availability_json = json.dumps(booking_availability)

            with DatabaseConnection(self.db_dsn) as cursor:
                print("Executing query:", query)
                print("With parameters:", (x_min, x_max, y_min, y_max, availability_json, map_hash))
                cursor.execute(query, (
                    x_min,
                    x_max,
                    y_min,
                    y_max,
                    availability_json,
                    map_hash
                ))
                result = cursor.fetchone()

                print("Result of query:", result)

                if result:
                    booking_object_hash = str(result['booking_object_hash'])
                    print(f"Обновленный объект: {booking_object_hash}")
                    return booking_object_hash
                else:
                    print(f"Объект с map_hash {map_hash} не найден, создаем новый.")
                    return self.create_booking_object(map_hash, x_min, x_max, y_min, y_max, booking_availability)
        except ValueError as ve:
            print(f"Ошибка преобразования данных: {ve}")
            raise ve
        except Exception as e:
            print(f"Ошибка при сохранении или обновлении объекта бронирования: {e}")
            raise e

    def delete_booking_object(self, map_hash: str, booking_object_hash: str) -> bool:
        """
        Удаляет объект бронирования по хешу объекта и хешу карты.

        :param map_hash: Хеш карты.
        :param booking_object_hash: Хеш объекта бронирования.
        :return: True, если объект удален, False, если объект не найден.
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
        query = """
                SELECT booking_object_hash, x_min, x_max, y_min, y_max
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
                        "y_max": row["y_max"]
                    }
                    for row in results
                ]

                return booking_objects
        except Exception:
            raise

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
