from typing import Optional
from django.http import JsonResponse
from django.http.request import HttpRequest
from django.utils.decorators import method_decorator
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status

from Bronyumo.settings import db_dsn
from apps.accounts.managers import CompanyManager, CompanySessionManager
from apps.utils.decorators import session_required


@method_decorator(session_required, name='dispatch')
class EditAvailableObjectsPanelView(View):
    def __init__(self, **kwargs: Optional[dict]) -> None:
        """
        Initializes the view. Sets up the company and session managers for use.

        :param kwargs: Additional keyword arguments passed to the parent class.
        """
        try:
            super().__init__(**kwargs)
            self.company_manager = CompanyManager(db_dsn=db_dsn)
            self.session_manager = CompanySessionManager(db_dsn=db_dsn)
        except Exception as e:
            # print(f"Error during initialization: {str(e)}")
            raise

    def get(self, request: HttpRequest, booking_hash: str) -> JsonResponse:
        """
        Handles GET requests to retrieve company information based on the session ID.

        :param request: The HTTP request object.
        :param booking_hash: The unique booking hash provided in the URL (not used in the current implementation).
        :return: A JsonResponse with either the company name or an error message.
        """
        try:
            session_id: Optional[str] = request.COOKIES.get('session_id')

            company_data: Optional[dict] = self.company_manager.get_company_by_session_id(session_id)
            print(company_data)

            if not company_data:
                return JsonResponse({"error": "Company not found."}, status=status.HTTP_400_BAD_REQUEST)

            company_name: str = company_data.get("name")

            return JsonResponse({"message": f"Hello, {company_name}!"})

        except ObjectDoesNotExist as e:
            return JsonResponse({"error": "Company data not found."}, status=status.HTTP_404_NOT_FOUND)
        except KeyError as e:
            return JsonResponse({"error": f"Missing key: {str(e)}."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
