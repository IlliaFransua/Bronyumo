from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.utils.serializers import MapUploadSerializer

class MapUploadAPI(APIView):
    """
    API for loading maps.
    """
    @staticmethod
    def post(request, format=None):
        """
        Downloads the map and saves it.
        """
        serializer = MapUploadSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Map uploaded successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
