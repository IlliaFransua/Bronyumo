from django.utils.decorators import method_decorator
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from apps.utils.decorators import session_required
from apps.accounts.DatabaseConnection import DatabaseConnection
from apps.accounts.managers import CompanyManager, CompanySessionManager
from Bronyumo.settings import db_dsn
from apps.main.models import Map, BookingObject, BookingRecord, Companies, CompanyMap, CompanySession


# Example of model import
# from apps.main.models import yourModer


@method_decorator(session_required, name='dispatch')
class UploadAndDeleteBookingsAPI(View):
    def __init__(self, **kwargs: dict) -> None:
        """
        Initializes the SignInAPI class, setting up the necessary managers for handling company and session data.

        :param kwargs: Additional arguments passed to the parent class.
        """
        super().__init__(**kwargs)
        self.company_manager = CompanyManager(db_dsn=db_dsn)
        self.session_manager = CompanySessionManager(db_dsn=db_dsn)
    @staticmethod
    def delete(self, request, map_hash):
        company_id = request.session.get('company_id')
        if not company_id:
            return JsonResponse({'error': 'Company ID not found in session.'}, status=400)

        try:
            with DatabaseConnection(self.db_dsn) as cursor:
                try:
                    query = "DELETE FROM company_map WHERE company_id = %s AND map_hash = %s;"
                    cursor.execute(query, (company_id, map_hash))
                except Exception as e:
                    return JsonResponse({'error': f'Error deleting from company_map: {str(e)}'}, status=500)

                try:
                    query = """
                                DELETE FROM booking_records
                                WHERE booking_object_hash IN (
                                    SELECT booking_object_hash FROM booking_objects
                                    WHERE map_hash = %s
                                );
                            """
                    cursor.execute(query, (map_hash,))
                except Exception as e:
                    return JsonResponse({'error': f'Error deleting from booking_records: {str(e)}'}, status=500)

                try:
                    query = "DELETE FROM booking_objects WHERE map_hash = %s;"
                    cursor.execute(query, (map_hash,))
                except Exception as e:
                    return JsonResponse({'error': f'Error deleting from booking_objects: {str(e)}'}, status=500)

                try:
                    query = "DELETE FROM maps WHERE map_hash = %s;"
                    cursor.execute(query, (map_hash,))
                except Exception as e:
                    return JsonResponse({'error': f'Error deleting from maps: {str(e)}'}, status=500)

                return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
