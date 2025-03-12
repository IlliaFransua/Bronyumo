from typing import Dict, Tuple
from django.http.request import HttpRequest
from django.http.response import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
import json
from Bronyumo.settings import db_dsn
from apps.accounts.utils import check_password
from apps.accounts.managers import CompanyManager, CompanySessionManager


class SignInAPI(APIView):
    def __init__(self, **kwargs: dict) -> None:
        """
        Initializes the SignInAPI class, setting up the necessary managers for handling company and session data.

        :param kwargs: Additional arguments passed to the parent class.
        """
        super().__init__(**kwargs)
        self.company_manager = CompanyManager(db_dsn=db_dsn)
        self.session_manager = CompanySessionManager(db_dsn=db_dsn)

    def post(self, request: HttpRequest) -> JsonResponse:
        """
        Handles the POST request for company sign-in.

        Parameters:
            request (Request): The request containing the user's login data.

        Calls the following methods:
        - `parse_request_data`: Parses the incoming JSON request body.
        - `validate_data`: Validates the provided data for correctness.
        - `authenticate_company`: Authenticates the company by email and password.
        - `create_session`: Creates a session for the company if authentication succeeds.
        - `generate_response`: Generates the response to send back to the user.
        """
        try:
            data = self.parse_request_data(request)
            email, password = self.validate_data(data)
            company = self.authenticate_company(email)
            session_id, expires_at = self.create_session(company['id'], password, company)
            return self.generate_response(company, session_id, expires_at)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Wrong data format."}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(f"Unexpected error: {type(e).__name__}: {str(e)}")
            return JsonResponse({"error": "An unexpected error occurred."},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def parse_request_data(self, request: HttpRequest) -> Dict:
        """
        Parses the incoming JSON request body.

        :param request: The HTTP request object.
        :return: Parsed JSON data as a Python dictionary.
        """
        return json.loads(request.body)

    def validate_data(self, data: Dict) -> Tuple[str, str]:
        """
        Validates the provided data for correctness.

        :param data: Parsed JSON data.
        :return: A tuple (email, password) if valid, raises an error otherwise.
        """
        email = data.get("email", "").strip()
        password = data.get("password", "").strip()

        if not all([email, password]):
            raise ValueError("Both email and password are required.")

        return email, password

    def authenticate_company(self, email: str) -> Dict:
        """
        Authenticates the company by its email.

        :param email: The email address provided by the user.
        :return: Company data if found, raises an error otherwise.
        """
        company = self.company_manager.get_company_by_email(email)

        if not company:
            raise ValueError("Company not found.")
        if 'id' not in company:
            raise ValueError("Company data is incomplete.")

        return company

    def create_session(self, company_id: str, password: str, company: Dict) -> Tuple[str, str]:
        """
        Creates a session for the company if authentication succeeds.

        :param company_id: The company ID.
        :param password: The password provided by the user.
        :return: session_id and expires_at if successful, raises an error otherwise.
        """
        if not check_password(password, company['hashed_password']):
            raise ValueError("Invalid password.")

        result = self.session_manager.start_session(company_id)

        if result is None:
            raise ValueError("Failed to create session.")

        return result

    def generate_response(self, company: Dict, session_id: str, expires_at: str) -> JsonResponse:
        """
        Generates the response to send back to the user.

        :param company: The authenticated company data.
        :param session_id: The session ID for the company.
        :param expires_at: The session expiration timestamp.
        :return: JsonResponse containing the login success message and session details.
        """
        response = JsonResponse({
            "message": "Company successfully logged in.",
            "company_id": company['id'],
            "session_id": session_id,
            "expires_at": expires_at.isoformat()
        }, status=status.HTTP_200_OK)

        response.set_cookie('session_id', session_id, expires=expires_at, httponly=True, secure=True)

        return response
