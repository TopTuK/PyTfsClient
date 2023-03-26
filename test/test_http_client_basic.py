import context
import unittest
import warnings
from pytfsclient.services.http.http_client import HttpClient

# https://stackoverflow.com/questions/5725430/http-test-server-accepting-get-post-requests
class HttpClientBasicTests(unittest.TestCase):

    def setUp(self):
        warnings.simplefilter('ignore', category=ResourceWarning)

        self.base_url = 'https://httpbin.org/'

        self.get_action = 'get'
        self.post_action = 'post'
        self.patch_action = 'patch'

        self.http_client: HttpClient = HttpClient(self.base_url, verify=True)

    # GET request test
    def test_get_request_success(self):
        # Arrange

        # Act
        http_response = self.http_client.get(self.get_action)

        # Assert
        self.assertIsNotNone(http_response, 'HTTP Response is None')
        self.assertIsNotNone(http_response.content, 'HTTP Response content is None')
    
    # GET Returns json response with args
    def test_get_requests_args_success(self):

        # Arrange
        args = {
            "id": "1",
            "my_param": "my_value"
        }

        # Act
        http_response = self.http_client.get(self.get_action, query_params=args)

        # Assert
        self.assertIsNotNone(http_response, 'HTTP Response is None')
        self.assertIsNotNone(http_response.content, 'HTTP Response content is None')

        content = http_response.json()
        self.assertIsNotNone(content, 'Can\'t convert HTTP content to json')
        self.assertIsNotNone(content['args'], 'HTTP Content args are None')
        
        self.assertEqual(content['args']['id'], args['id'])
        self.assertEqual(content['args']['my_param'], args['my_param'])

    # POST request. Returns success response
    def test_post_request_success(self):
        # Arrange

        # Act
        http_response = self.http_client.post(self.post_action, None)

        # Assert
        self.assertIsNotNone(http_response, 'HTTP Response is None')
        self.assertIsNotNone(http_response.content, 'HTTP Response content is None')

    # POST request. Returns json response with args
    def test_post_request_args_success(self):
        # Arrange
        args = {
            "id": "1",
            "my_param": "my_value"
        }

        # Act
        http_response = self.http_client.post(self.post_action, args)

        # Assert
        self.assertIsNotNone(http_response, 'HTTP Response is None')
        self.assertIsNotNone(http_response.content, 'HTTP Response content is None')

        content = http_response.json()
        self.assertIsNotNone(content, 'Can\'t convert HTTP content to json')
        self.assertIsNotNone(content['form'], 'HTTP Content args are None')
        
        self.assertEqual(content['form']['id'], args['id'])
        self.assertEqual(content['form']['my_param'], args['my_param'])

    # POST JSON request. Returns json response with args
    def test_post_json_request_success(self):
        # Arrange
        json = [
            {
                "A": "AA",
                "B": "BB",
            },
            {
                "C": True,
                "D": 1,
            }
        ]

        # Act
        http_response = self.http_client.post_json(self.post_action, json_data=json)

        # Assert
        self.assertIsNotNone(http_response, 'HTTP Response is None')
        self.assertIsNotNone(http_response.content, 'HTTP Response content is None')

        content = http_response.json()
        self.assertIsNotNone(content, 'Can\'t convert HTTP content to json')
        self.assertIsNotNone(content['json'], 'HTTP json content does not have json elem')

        self.assertEqual(2, len(content['json']))
    
    # PATCH request Returns success response
    def test_patch_request_success(self):
        # Arrange

        # Act
        http_response = self.http_client.patch(self.patch_action, None)

        # Assert
        self.assertIsNotNone(http_response, 'HTTP Response is None')
        self.assertIsNotNone(http_response.content, 'HTTP Response content is None')

    # patch JSON request. Returns json response with args
    def test_patch_json_request_success(self):
        # Arrange
        json = [
            {
                "A": "AA",
                "B": "BB",
            },
            {
                "C": True,
                "D": 1,
            }
        ]

        # Act
        http_response = self.http_client.patch_json(self.patch_action, json_data=json)

        # Assert
        self.assertIsNotNone(http_response, 'HTTP Response is None')
        self.assertIsNotNone(http_response.content, 'HTTP Response content is None')

        content = http_response.json()
        self.assertIsNotNone(content, 'Can\'t convert HTTP content to json')
        self.assertIsNotNone(content['json'], 'HTTP json content does not have json elem')

        self.assertEqual(2, len(content['json']))


# Executing the tests in the above test case class
if __name__ == "__main__":
    unittest.main(verbosity=2)