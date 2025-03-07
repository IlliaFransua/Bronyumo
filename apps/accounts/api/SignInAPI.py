from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from apps.accounts.serializers import SignInSerializer


class SignInAPI(APIView):
    """
    API-endpoint for user authentication (sign-in).
    """
    @staticmethod
    def post(request, format=None):
        """
        Handle POST requests for user sign-in.

        This method authenticates the user using the provided credentials.
        If authentication is successful, it returns an authentication token.
        Otherwise, it returns an error response.

        Args:
            request: The HTTP request object containing the login credentials.
            format: Optional format for the response (default is None).

        Returns:
            Response: A JSON response indicating the result of authentication.
                - On success: HTTP 200 OK with an authentication token.
                - On failure: HTTP 400 Bad Request with an error message.
        """
        serializer = SignInSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)

            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response(
                    {'message': 'Login successful', 'token': token.key},
                    status=status.HTTP_200_OK
                )
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
