import json
from datetime import datetime
from typing import Dict
from uuid import UUID

from django.http.request import HttpRequest
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.views import APIView

from Bronyumo.settings import db_dsn
from apps.accounts.managers import CompanyManager, CompanySessionManager
from apps.accounts.utils import check_password


class SignInAPI(APIView):
    def __init__(self, **kwargs: dict) -> None:
        """
        Initializes the SignInAPI class.

        :param kwargs: Additional keyword arguments.
        """
        super().__init__(**kwargs)
        self.company_manager = CompanyManager(db_dsn=db_dsn)
        self.session_manager = CompanySessionManager(db_dsn=db_dsn)

    def post(self, request: HttpRequest) -> JsonResponse:
        """
        Handles the POST request for user authentication.

        Parameters:
            request (HttpRequest): The request containing user login credentials.

        Returns:
            JsonResponse: The authentication result or error message.

        Expected data format:
            {
                "email": <string>,
                "password": <string>
            }

        Expected result on successful authentication:
            {
                "message": "Company successfully logged in.",
                "company_id": <int>,
                "session_id": <string>,
                "expires_at": <ISO 8601>
            }

        In case of authentication failure:
            {
                "error": <string>
            }
        """
        try:
            data = self.parse_request_data(request)
            email = data.get("email", "").strip()
            password = data.get("password", "").strip()
            company = self.authenticate_company(email, password)
            session_id, expires_at = self.create_session(company['id'])
            return self.generate_response(company, session_id, expires_at)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Wrong data format."}, status=status.HTTP_400_BAD_REQUEST)

        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return JsonResponse({"error": f"{e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def parse_request_data(self, request: HttpRequest) -> Dict:
        """
        Parses the incoming JSON request body.

        :param request: HttpRequest object containing the request data.
        :return: Dictionary with parsed JSON data.
        """
        try:
            return json.loads(request.body)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format.")

    def authenticate_company(self, email: str, password: str) -> Dict:
        """
        Authenticates the company using the provided email and password.

        :param email: Company email address.
        :param password: Plaintext password for authentication.
        :return: Dictionary containing company details if authentication is successful.
        """
        company = self.company_manager.get_company_by_email(email)
        if not company:
            raise ValueError("Company not found.")

        if 'id' not in company or 'hashed_password' not in company:
            raise ValueError("Company data is incomplete.")

        if not check_password(password, company['hashed_password']):
            raise ValueError("Invalid password.")

        return company

    def create_session(self, company_id: int) -> tuple[UUID, datetime]:
        """
        Creates a session for the authenticated company.

        :param company_id: ID of the authenticated company.
        :return: Tuple containing session UUID and expiration datetime.
        """
        result = self.session_manager.start_session(company_id)
        if result is None:
            raise ValueError("Failed to create session.")

        return result

    def generate_response(self, company: Dict, session_id: UUID, expires_at: datetime) -> JsonResponse:
        """
        Generates the response containing session details.

        :param company: Dictionary with authenticated company details.
        :param session_id: UUID of the created session.
        :param expires_at: Expiration datetime of the session.
        :return: JsonResponse with session details.
        """
        response = JsonResponse({
            "message": "Company successfully logged in.",
            "company_id": company['id'],
            "session_id": session_id,
            "expires_at": expires_at.isoformat()
        }, status=status.HTTP_200_OK)

        response.set_cookie('session_id', session_id, expires=expires_at, httponly=True, secure=True)

        return response
