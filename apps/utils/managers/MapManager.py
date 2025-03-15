from apps.accounts.DatabaseConnection import DatabaseConnection
import psycopg2

class MapManager:
    def __init__(self,db_dsn: str):
        self.db_dsn = db_dsn

    def get_map_hash_by_route(self, map_route: str):
        query = f'SELECT map_hash FROM public.maps WHERE image_path = %s'
        #print(f'db test')
        with DatabaseConnection(self.db_dsn) as cursor:
            cursor.execute(query, (map_route,))
            map_hash = cursor.fetchone()
            #print(f'map_hash : {map_hash}')
            return map_hash[0] if map_hash else None
    
    def save_map_route(self, map_route: str, company_id: int):
        query_save_in_map_table = f'INSERT INTO public.maps (image_path) VALUES (%s) RETURNING map_hash'
        #print(f'Testing db_dsn: {self.db_dsn}')

        with DatabaseConnection(self.db_dsn) as cursor:
            cursor.execute(query_save_in_map_table, (map_route,))
            result = cursor.fetchone()
            #print(f"Query result: {result}")
            map_hash = result["map_hash"]
            #print(f"map_hash : {map_hash}")

        query_save_map_company_reference = f'INSERT INTO public.company_map (company_id, map_hash) VALUES (%s,%s)'
        with DatabaseConnection(self.db_dsn) as cursor:
            cursor.execute(query_save_map_company_reference, (company_id,map_hash,))
        return map_hash