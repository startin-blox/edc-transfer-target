from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
from django.urls import reverse
from django.conf import settings
import os
from django.views.decorators.csrf import csrf_exempt

from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from .models import StoredFile

class JSONToFile(APIView):
    authentication_classes = [] #disables authentication
    permission_classes = [] #disables permission

    @csrf_exempt
    @extend_schema(
        request=[],
        parameters=[],
        examples=[
            OpenApiExample(
                "JSONToFileExample",
                value={
                    'message': 'Hello, world!'
                },
                request_only=True,
                response_only=False
            )
        ],
        responses={
            201: OpenApiResponse(description='File saved successfully'),
            400: OpenApiResponse(description='Invalid input data.'),
        }
    )
    def post(self, request, filename):
        try:
            # Get JSON data from request
            json_data = json.loads(request.body)

            # Write JSON data to file
            filepath = os.path.join(settings.MEDIA_ROOT, filename)
            with open(filepath, 'w') as outfile:
                json.dump(json_data, outfile)

            # Get URL of saved file
            file_url = request.build_absolute_uri(reverse('sink', args=[filename]))

            # Create a new instance of the StoredFile model
            stored_file = StoredFile()

            # Set the original_filename and url fields
            stored_file.original_filename = filename
            stored_file.url = file_url
            stored_file.path = filepath

            # Save the new instance to the database
            stored_file.save()

            # Return success response with URL of saved file
            return Response({'message': 'File saved successfully', 'file_url': file_url}, status=status.HTTP_201_CREATED)


        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @csrf_exempt
    @extend_schema(
        request=[],
        parameters=[],
        responses={
            201: OpenApiResponse(description='File saved successfully'),
            400: OpenApiResponse(description='Invalid input data.'),
        }
    )
    def get(self, request, filename):
        try:
            # Check if file exists
            # Retrieve an instance of the StoredFile model by ID
            stored_file = StoredFile.objects.get(original_filename=filename)

            if not stored_file:
                return Response({'message': 'File not found'}, status=status.HTTP_404_NOT_FOUND)


            # Access the original_filename and url fields
            filename = stored_file.original_filename

            # Read JSON data from file
            with open(stored_file.path, 'r') as infile:
                json_data = json.load(infile)

            return Response(json_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)
