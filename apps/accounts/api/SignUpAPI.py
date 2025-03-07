from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.accounts.serializers import SignUpSerializer


class SignUpAPI(APIView):
    """
    API-endpoint for new user registration.
    """
    @staticmethod
    def post(self, request, format=None):
        """
        Handle POST requests for user sign-up.

        This method processes incoming sign-up requests by validating the provided
        data against the SignUpSerializer. If the data is valid, a new user is created
        and a success response is returned with the username. If the data is invalid,
        an error response is returned with the validation errors.

        Args:
            request: The HTTP request object containing the sign-up data.
            format: Optional format for the response (default is None).

        Returns:
            Response: A JSON response indicating the result of the sign-up process.
                - On success: HTTP 201 Created with a message and the username.
                - On failure: HTTP 400 Bad Request with validation errors.
        """
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {'message': 'User created successfully', 'username': user.username},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
