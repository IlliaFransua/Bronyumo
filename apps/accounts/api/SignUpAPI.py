import json
from datetime import datetime
from typing import Dict, Tuple
from typing import Union
from urllib.request import Request

from django.core.exceptions import ValidationError
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from Bronyumo.settings import db_dsn
from apps.accounts.managers import CompanyManager, CompanySessionManager
from apps.accounts.utils import hash_password
from apps.accounts.validators import PasswordStrengthValidator, EmailValidator


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

            error = self.validate_fields(company_name, address, email, password)
            if error:
                return JsonResponse({"error": error}, status=status.HTTP_400_BAD_REQUEST)

            if self.company_manager.company_exists(email):
                return JsonResponse({"error": "Company with such email already exists."},
                                    status=status.HTTP_400_BAD_REQUEST)

            hashed_password = self.hash_password(password)

            company_id = self.create_company(company_name, address, email, hashed_password)
            if company_id is None:
                return JsonResponse({"error": "Company with such email already exists."},
                                    status=status.HTTP_400_BAD_REQUEST)

            session_id, expires_at = self.create_session(company_id)
            if session_id is None:
                return JsonResponse({"error": "Failed to create session."},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return self.generate_response(company_id, session_id, expires_at)

        except Exception as e:
            return JsonResponse({"error": f"{e}"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def parse_request_data(self, request: Request) -> Dict:
        """
        Parses the incoming JSON request body.

        Parameters:
            request (Request): The HTTP request object.

        Returns:
            Dict: The parsed JSON data as a Python dictionary.
        """
        try:
            return json.loads(request.body)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format.")

    def extract_fields(self, data: Dict) -> Tuple[str, str, str, str]:
        """
        Extracts the required fields from the provided data.

        Parameters:
            data (Dict): Parsed JSON data.

        Returns:
            Tuple[str, str, str, str]: A tuple containing company_name, address, email, and password.
        """
        return (
            data.get("companyName", "").strip(),
            data.get("address", "").strip(),
            data.get("email", "").strip(),
            data.get("password", "").strip(),
        )

    def validate_fields(self, company_name: str, address: str, email: str, password: str) -> Union[Response, None]:
        """
        Validates that all required fields are provided.

        Parameters:
            company_name (str): The company name provided by the user.
            address (str): The company address.
            email (str): The company email.
            password (str): The company password.

        Returns:
            str | None: Error message if validation fails, otherwise None.
        """
        if not company_name:
            return Response({"error": "Company name is required."}, status=status.HTTP_400_BAD_REQUEST)

        if not address:
            return Response({"error": "Address is required."}, status=status.HTTP_400_BAD_REQUEST)

        if not email:
            return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                EmailValidator().validate(email)
            except ValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if not password:
            return Response({"error": "Password is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            PasswordStrengthValidator().validate(password)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return None

    def hash_password(self, password: str) -> str:
        """
        Hashes the password before storing it.

        Parameters:
            password (str): The password provided by the user.

        Returns:
            str: The hashed password.
        """
        return hash_password(password)

    def create_company(self, company_name: str, address: str, email: str, hashed_password: str) -> int:
        """
        Creates a new company record in the database.

        Parameters:
            company_name (str): The company name.
            address (str): The company address.
            email (str): The company email.
            hashed_password (str): The hashed password.

        Returns:
            int: The company ID if creation is successful.

        Raises:
            ValueError: If company creation fails.
        """
        try:
            company_id = self.company_manager.create_company(company_name, address, email, hashed_password)
            if not company_id:
                raise ValueError("Failed to create company.")
            return company_id
        except Exception as e:
            raise ValueError(f"Error creating company: {e}")

    def create_session(self, company_id: int) -> Union[Tuple[str, datetime], None]:
        """
        Creates a session for the newly created company.

        Parameters:
            company_id (int): The ID of the created company.

        Returns:
            Tuple[UUID, datetime] | None: A tuple (session_id, expires_at) if successful.

        Raises:
            ValueError: If session creation fails.
        """
        try:
            session_id, expires_at = self.session_manager.start_session(company_id)
            if not session_id or not expires_at:
                raise ValueError("Session creation failed due to missing session ID or expiration time.")
            return session_id, expires_at
        except Exception as e:
            raise ValueError(f"Error creating session: {e}")

    def generate_response(self, company_id: int, session_id: str, expires_at: datetime) -> JsonResponse:
        """
        Generates the response to send back to the user.
    
        Parameters:
            company_id (int): The ID of the created company.
            session_id (UUID): The session ID for the company.
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

        response.set_cookie('session_id', session_id, expires=expires_at, httponly=True, secure=True, samesite="Strict")

        return response
