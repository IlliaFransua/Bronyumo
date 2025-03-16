import os
from typing import Optional

from Bronyumo.settings import db_dsn
from apps.accounts.managers import MapManager
from apps.utils.decorators import session_required
from django.conf.global_settings import MEDIA_ROOT
from django.http import FileResponse, Http404
from django.utils.decorators import method_decorator
from rest_framework.views import APIView


@method_decorator(session_required, name='dispatch')
class GetMapImageAPI(APIView):
    """
    API endpoint for retrieving a map image by its hash.
    Ensures that the map belongs to the requesting company.
    """

    def __init__(self, **kwargs: Optional[dict]) -> None:
        super().__init__(**kwargs)
        self.map_manager = MapManager(db_dsn=db_dsn)

    def get(self, request, map_hash: str):
        """
        Handles GET requests to retrieve the image file for a given map hash.

        Parameters:
            request (HttpRequest): The HTTP request object with session cookies.
            map_hash (str): The unique identifier of the map.

        Returns:
            FileResponse: The image file response if found.
            Http404: If the image does not exist or map does not belong to the company.
        """
        try:
            image_path = self.map_manager.get_map_image_path(map_hash)
            if not image_path:
                raise Http404("Image not found.")

            full_image_path = os.path.join(MEDIA_ROOT, image_path)
            if not os.path.exists(full_image_path):
                raise Http404("File does not exist.")

            return FileResponse(open(full_image_path, 'rb'), content_type='image/jpeg')
        except Exception:
            raise Http404("Error retrieving the image.")
