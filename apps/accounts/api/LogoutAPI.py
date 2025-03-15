from typing import Optional

from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.views import APIView

from Bronyumo.settings import db_dsn
from apps.accounts.managers import CompanySessionManager


class LogoutAPI(APIView):
    """
    API for session termination (logout).
    """

    def __init__(self, **kwargs: Optional[dict]) -> None:
        """
        Initializes the logout API.

        Parameters:
            kwargs (Optional[dict]): Additional parameters passed to the parent class.
        """
        super().__init__(**kwargs)
        self.session_manager = CompanySessionManager(db_dsn=db_dsn)

    def get(self, request) -> JsonResponse:
        """
        Handles the GET request for logging out.

        Checks for the session ID in cookies and terminates the session if found.

        Parameters:
            request: The HTTP request object.

        Returns:
            JsonResponse: A success message if logout is successful, otherwise an error message.
        """
        try:
            session_id: Optional[str] = request.COOKIES.get('session_id')

            if not session_id:
                return JsonResponse({"error": "Session not found."}, status=status.HTTP_400_BAD_REQUEST)

            session_deleted = self.session_manager.delete_session_by_id(session_id)

            if session_deleted:
                response = JsonResponse({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
                response.delete_cookie('session_id')
                return response
            else:
                return JsonResponse({"error": "Failed to log out."}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return JsonResponse({"error": f"An unexpected error occurred: {str(e)}"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
