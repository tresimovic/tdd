"""
Test Cases for Counter Web Service

Create a service that can keep a track of multiple counters
- API must be RESTful - see the status.py file. Following these guidelines, you can make assumptions about
how to call the web service and assert what it should return.
- The endpoint should be called /counters
- When creating a counter, you must specify the name in the path.
- Duplicate names must return a conflict error code.
- The service must be able to update a counter by name.
- The service must be able to read the counter
"""

from unittest import TestCase

# we need to import the unit under test - counter
from src.counter import app 

# we need to import the file that contains the status codes
from src import status 

class CounterTest(TestCase):
    """Counter tests"""
    
    def test_create_a_counter(self):
        """It should create a counter"""
        client = app.test_client()
        result = client.post('/counters/foo')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

    def setUp(self):
        self.client = app.test_client()

    def test_duplicate_a_counter(self):
        """It should return an error for duplicates"""
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_409_CONFLICT)

    def test_update_a_counter(self):
        """It should create a counter and update it"""
        post_result = self.client.post('/counters/test')
        self.assertEqual(post_result.status_code, status.HTTP_201_CREATED)
        baseline_result = self.client.get('/counters/test')
        self.assertEqual(baseline_result.status_code, status.HTTP_200_OK)
        baseline_value = baseline_result.json
        self.assertEqual(baseline_value['test'], 0)
        put_result = self.client.put('/counters/test')
        self.assertEqual(put_result.status_code, status.HTTP_200_OK)
        updated_result = self.client.get('/counters/test')
        self.assertEqual(updated_result.status_code, status.HTTP_200_OK)
        updated_value = updated_result.json
        self.assertEqual(updated_value['test'], baseline_value['test']+1)

    def test_read_a_counter(self):
        """It should create a counter and read it"""
        post_result = self.client.post('/counters/new')
        self.assertEqual(post_result.status_code, status.HTTP_201_CREATED)
        get_result = self.client.get('/counters/new')
        self.assertEqual(get_result.status_code, status.HTTP_200_OK)
