import os
import uuid
from typing import Optional

from Bronyumo.settings import db_dsn
from apps.accounts.managers import CompanyManager, CompanySessionManager
from apps.utils.decorators import session_required
from apps.utils.managers import MapManager
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.views import APIView


@method_decorator(session_required, name='dispatch')
class MapUploadAPI(APIView):
    def __init__(self, **kwargs: Optional[dict]) -> None:
        super().__init__(**kwargs)
        self.map_manager = MapManager(db_dsn=db_dsn)
        self.company_manager = CompanyManager(db_dsn=db_dsn)
        self.session_manager = CompanySessionManager(db_dsn=db_dsn)

    def post(self, request, *args, **kwargs):
        try:
            session_id: Optional[str] = request.COOKIES.get('session_id')
            company_data: Optional[dict] = self.company_manager.get_company_by_session_id(session_id)

            if not company_data:
                return JsonResponse({"error": "Company not found."}, status=status.HTTP_400_BAD_REQUEST)

            company_id = company_data.get("id")

            uploaded_file = request.FILES.get('floorPlanImage')
            if not uploaded_file:
                return JsonResponse({"error": "No file provided."}, status=status.HTTP_400_BAD_REQUEST)

            upload_dir = f'uploads/maps/{company_id}/'

            file_extension = os.path.splitext(uploaded_file.name)[1]
            unique_filename = str(uuid.uuid4()) + file_extension
            file_path = os.path.join(upload_dir, unique_filename)

            counter = 0
            while default_storage.exists(file_path) and counter < 100:
                unique_filename = str(uuid.uuid4()) + file_extension
                file_path = os.path.join(upload_dir, unique_filename)
                counter += 1

            if (counter == 100):
                print("can't create unique name for file")
                return JsonResponse({"error": f"can't create unique name for file"},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            default_storage.save(file_path, ContentFile(uploaded_file.read()))

            try:
                map_hash = self.map_manager.save_map_route(file_path, company_id)
            except Exception as e:
                print("Database save error: {str(e)}")
                return JsonResponse({"error": f"Database save error: {str(e)}"},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            redirect_url = reverse('edit-available-objects-panel-view-with-hash', kwargs={'map_hash': map_hash})
            return JsonResponse({
                "map_hash": str(map_hash),
                "redirect_url": redirect_url
            }, status=status.HTTP_201_CREATED)

        except ObjectDoesNotExist as e:
            return JsonResponse({"error": "Company data not found."}, status=status.HTTP_404_NOT_FOUND)
        except KeyError as e:
            return JsonResponse({"error": f"Missing key: {str(e)}."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("An unexpected error occurred: " + str(e))
            return JsonResponse({"error": "An unexpected error occurred: " + str(e)},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
