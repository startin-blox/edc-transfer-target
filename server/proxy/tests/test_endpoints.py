from django.test import TestCase, Client
from rest_framework import status
import json

class JSONToFileTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_save_json_file_success(self):
        # Test saving a JSON file with a valid filename and data
        filename = 'test_file.json'
        data = {'message': 'Hello, world!'}
        response = self.client.post('/sink/{}'.format(filename), json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_save_json_file_error(self):
        # Test saving a JSON file with an invalid filename
        filename = 'test_file.pdf'
        data = 'zpdkaokdpaozjdapdjzdpojajodazjd'
        response = self.client.post('/sink/{}'.format(filename), data, content_type='application/pdf')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_load_json_file_success(self):
        # Test saving file first, we need it to exist
        filename = 'test_file.json'
        data = {'message': 'Hello, world!'}
        response = self.client.post('/sink/{}'.format(filename), json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Test loading a JSON file with a valid filename
        filename = 'test_file.json'
        response = self.client.get('/sink/{}'.format(filename))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), {'message': 'Hello, world!'})

    def test_load_json_file_error(self):
        # Test loading a non-existent JSON file
        filename = 'nonexistent_file.json'
        response = self.client.get('/sink/{}'.format(filename))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)