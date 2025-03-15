import os
from typing import Optional
import uuid
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import status
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist

from Bronyumo.settings import db_dsn
from apps.accounts.managers import CompanyManager, CompanySessionManager
from apps.utils.managers import MapManager
from apps.utils.decorators import session_required


@method_decorator(session_required, name='dispatch')
class MapUploadAPI(APIView):
    def __init__(self, **kwargs: Optional[dict]) -> None:
        super().__init__(**kwargs)
        self.map_manager = MapManager(db_dsn=db_dsn)
        self.company_manager = CompanyManager(db_dsn=db_dsn)
        self.session_manager = CompanySessionManager(db_dsn=db_dsn)

    def post(self, request, *args, **kwargs):
        #print("Start debugging...", flush=True)
        try:
            session_id: Optional[str] = request.COOKIES.get('session_id')
            company_data: Optional[dict] = self.company_manager.get_company_by_session_id(session_id)

            if not company_data:
                return JsonResponse({"error": "Company not found."}, status=status.HTTP_400_BAD_REQUEST)

            company_id = company_data.get("id")

            # Отримуємо файл із запиту
            uploaded_file = request.FILES.get('floorPlanImage')
            if not uploaded_file:
                return JsonResponse({"error": "No file provided."}, status=status.HTTP_400_BAD_REQUEST)

            # Make dir for file
            upload_dir = f'uploads/maps/{company_id}/'

            # creating unique file name
            file_extension = os.path.splitext(uploaded_file.name)[1]
            unique_filename = str(uuid.uuid4()) + file_extension
            file_path = os.path.join(upload_dir, unique_filename)

            print(f"File extension: {file_path}")

            # check file exist loop
            counter = 0
            while default_storage.exists(file_path) and counter < 100:
                unique_filename = str(uuid.uuid4()) + file_extension
                file_path = os.path.join(upload_dir, unique_filename)
                counter += 1
            if(counter == 100):
                return JsonResponse({"error": f"can't create unique name for file"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            # save file
            default_storage.save(file_path, ContentFile(uploaded_file.read()))

            # Додаємо запис у таблицю maps
            print(f"File successfully saved at: {file_path}")  # Файл збережено
            try:
                map_hash = self.map_manager.save_map_route(file_path, company_id)
                print(f"Map saved to DB with hash: {map_hash}")  # Якщо успішно
            except Exception as e:
                print(f"Database save error: {e}")  # Вивід помилки
                return JsonResponse({"error": f"Database save error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


            # Повертаємо map_hash
            return JsonResponse({"map_hash": str(map_hash)}, status=status.HTTP_201_CREATED)

        except ObjectDoesNotExist as e:
            return JsonResponse({"error": "Company data not found."}, status=status.HTTP_404_NOT_FOUND)
        except KeyError as e:
            return JsonResponse({"error": f"Missing key: {str(e)}."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


