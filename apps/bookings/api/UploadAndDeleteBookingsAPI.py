from django.utils.decorators import method_decorator
from django.views import View
from typing import Optional
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from apps.utils.decorators import session_required
from rest_framework import status
from rest_framework.views import APIView
from apps.accounts.DatabaseConnection import DatabaseConnection
from apps.accounts.managers import CompanyManager, CompanySessionManager
from Bronyumo.settings import db_dsn


# Example of model import
# from apps.main.models import yourModer


@method_decorator(session_required, name='dispatch')
class UploadAndDeleteBookingsAPI(APIView):
    def __init__(self, **kwargs: dict) -> None:
        """
        Initializes the SignInAPI class, setting up the necessary managers for handling company and session data.

        :param kwargs: Additional arguments passed to the parent class.
        """
        super().__init__(**kwargs)
        self.db_dsn = db_dsn
        self.company_manager = CompanyManager(db_dsn=db_dsn)
        self.session_manager = CompanySessionManager(db_dsn=db_dsn)
    def delete(self, request, map_hash):
        try:
            session_id: Optional[str] = request.COOKIES.get('session_id')
            company_data: Optional[dict] = self.company_manager.get_company_by_session_id(session_id)

            if not company_data:
                return JsonResponse({"error": "Company not found."}, status=status.HTTP_400_BAD_REQUEST)

            company_id = company_data.get("id")
        except ObjectDoesNotExist as e:
            return JsonResponse({"error": "Company data not found."}, status=status.HTTP_404_NOT_FOUND)
        except KeyError as e:
            return JsonResponse({"error": f"Missing key: {str(e)}."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

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
