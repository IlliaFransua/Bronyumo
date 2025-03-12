from datetime import datetime
from urllib.request import Request
from django.http.response import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
import json
from Bronyumo.settings import db_dsn
from apps.accounts.utils import hash_password
from apps.accounts.managers import CompanyManager, CompanySessionManager
from typing import Dict, Tuple


class SignUpAPI(APIView):
    """
    This API endpoint is responsible for creating a new user account.
    It uses validation algorithms to ensure correct registration processes.

    Key features:
    - Receives a POST request with registration data.
    - Checks the uniqueness of the user account.
    - Hashes the password before saving.
    - Creates a new record in the database.
    - Returns confirmation of successful registration or an error.
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.company_manager = CompanyManager(db_dsn=db_dsn)
        self.session_manager = CompanySessionManager(db_dsn=db_dsn)

    def post(self, request: Request) -> JsonResponse:
        """
        Handles the POST request for user registration.

        Parameters:
            request (Request): The user data provided for registration.

        Returns:
            JsonResponse: The registration result or error message.

        Expected data format:
            {
                "companyName": <string>,
                "address": <string>,
                "email": <string>,
                "password": <string>
            }

        Expected result on successful registration:
            {
                "message": "Company successfully established.",
                "company_id": <string>,
                "session_id": <string>,
                "expires_at": <ISO 8601>
            }

        In case of registration error:
            {
                "error": <string>
            }
        """
        try:
            data = self.parse_request_data(request)
            company_name, address, email, password = self.extract_fields(data)
            self.validate_fields(company_name, address, email, password)
            hashed_password = self.hash_password(password)
            company_id = self.create_company(company_name, address, email, hashed_password)
            self.check_if_company_exists(company_id)
            session_id, expires_at = self.create_session(company_id)
            return self.generate_response(company_id, session_id, expires_at)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Wrong data format."}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # print(f"Unexpected error: {type(e).__name__}: {str(e)}")
            return JsonResponse({"error": "An unexpected error occurred."},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def parse_request_data(self, request: Request) -> Dict:
        """
        Parses the incoming JSON request body.

        Parameters:
            request (Request): The HTTP request object.

        Returns:
            Dict: The parsed JSON data as a Python dictionary.
        """
        return json.loads(request.body)

    def extract_fields(self, data: Dict) -> Tuple[str, str, str, str]:
        """
        Extracts the required fields from the provided data.

        Parameters:
            data (Dict): Parsed JSON data.

        Returns:
            Tuple[str, str, str, str]: A tuple containing company_name, address, email, and password.
        """
        company_name = data.get("companyName", "").strip()
        address = data.get("address", "").strip()
        email = data.get("email", "").strip()
        password = data.get("password", "").strip()

        return company_name, address, email, password

    def validate_fields(self, company_name: str, address: str, email: str, password: str) -> None:
        """
        Validates that all required fields are provided.

        Parameters:
            company_name (str): The company name provided by the user.
            address (str): The company address.
            email (str): The company email.
            password (str): The company password.

        Raises:
            ValueError: If any field is missing.
        """
        if not all([company_name, address, email, password]):
            raise ValueError("All fields are required.")

    def hash_password(self, password: str) -> str:
        """
        Hashes the password before storing it.

        Parameters:
            password (str): The password provided by the user.

        Returns:
            str: The hashed password.
        """
        return hash_password(password)

    def create_company(self, company_name: str, address: str, email: str, hashed_password: str) -> str:
        """
        Creates a new company record in the database.

        Parameters:
            company_name (str): The company name.
            address (str): The company address.
            email (str): The company email.
            hashed_password (str): The hashed password.

        Returns:
            str: The company ID if creation is successful.
        """
        return self.company_manager.create_company(company_name, address, email, hashed_password)

    def check_if_company_exists(self, company_id: str) -> None:
        """
        Checks if a company with the provided email already exists.

        Parameters:
            company_id (str): The ID of the created company.

        Raises:
            ValueError: If the company with the same email already exists.
        """
        if company_id is None:
            raise ValueError("Company with such email already exists.")

    def create_session(self, company_id: str) -> Tuple[str, datetime]:
        """
        Creates a session for the newly created company.

        Parameters:
            company_id (str): The ID of the created company.

        Returns:
            Tuple[str, datetime]: A tuple (session_id, expires_at) if successful.

        Raises:
            ValueError: If session creation fails.
        """
        result = self.session_manager.start_session(company_id)

        if result is None:
            raise ValueError("Failed to create session.")

        return result

    def generate_response(self, company_id: str, session_id: str, expires_at: datetime) -> JsonResponse:
        """
        Generates the response to send back to the user.

        Parameters:
            company_id (str): The ID of the created company.
            session_id (str): The session ID for the company.
            expires_at (datetime): The session expiration timestamp.

        Returns:
            JsonResponse: The success response with session details.
        """
        response = JsonResponse({
            "message": "Company successfully established.",
            "company_id": company_id,
            "session_id": session_id,
            "expires_at": expires_at.isoformat()
        }, status=status.HTTP_201_CREATED)

        response.set_cookie('session_id', session_id, expires=expires_at, httponly=True, secure=True)

        return response

