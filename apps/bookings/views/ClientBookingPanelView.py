import json
from typing import Optional

from django.http import HttpResponse, JsonResponse, HttpRequest
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import status

from Bronyumo.settings import db_dsn
from apps.accounts.managers import CompanyManager, CompanySessionManager, MapManager
from apps.utils.decorators import session_required
import json
from typing import Optional

from Bronyumo.settings import db_dsn
from apps.accounts.managers import CompanyManager, CompanySessionManager, MapManager
from apps.utils.decorators import session_required
from django.http import JsonResponse
from django.http.request import HttpRequest
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import status


class ClientBookingPanelView(View):
    def get(self, request, map_hash):
        """
        Handle GET requests.

        This method processes GET requests and returns an HTML page.
        """
        return HttpResponse(f"Map Hash: {map_hash}")


@method_decorator(session_required, name='dispatch')
class ClientBookingPanelView(View):
    def __init__(self, **kwargs: Optional[dict]) -> None:
        """
        Initializes the view. Sets up the company and session managers for use.

        :param kwargs: Additional keyword arguments passed to the parent class.
        """
        try:
            super().__init__(**kwargs)
            self.company_manager = CompanyManager(db_dsn=db_dsn)
            self.session_manager = CompanySessionManager(db_dsn=db_dsn)
            self.map_manager = MapManager(db_dsn=db_dsn)
        except Exception as e:
            # print(f"Error during initialization: {str(e)}")
            raise

    def get(self, request: HttpRequest, map_hash: str):
        return render(request, "bookings/ClientBookingPanelView.html", )
