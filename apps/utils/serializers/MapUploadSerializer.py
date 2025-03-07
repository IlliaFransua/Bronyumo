from rest_framework import serializers

class MapUploadSerializer(serializers.ModelSerializer):
    @staticmethod
    def validate_file(value):
        """
        Checking the file for a valid format.
        """
        allowed_extensions = ['jpg', 'png']
        extension = value.name.split('.')[-1].lower()
        if extension not in allowed_extensions:
            raise serializers.ValidationError("Invalid file format. Allowed formats: jpg, png.")
        return value
