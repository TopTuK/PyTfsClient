import context
import unittest
from pytfsclient.client_factory import ClientFactory

class ClientConnectionTests(unittest.TestCase):
    def setUp(self):
        self.server_url = 'http://localhost/'
        
        self.collection = 'DefaultCollection'
        self.project = 'TestProject'
        self.project_name = f'{self.collection}/{self.project}'

        self.fake_pat = 'fakepat'
    
    # Basic client connection test with given params
    def test_create_client_connection(self):
        # Arrange
        api_url = f'{self.collection}/_apis/'
        project_api_url = f'{self.collection}/{self.project}/_apis/'

        # Act
        client_connection = ClientFactory.create_pat(self.fake_pat, self.server_url, self.project_name)

        # Assert
        self.assertEqual(client_connection.server_url, self.server_url)
        self.assertEqual(client_connection.collection, self.collection)
        self.assertEqual(client_connection.project_name, self.project)

        # Check server url
        self.assertIsNotNone(client_connection.http_client)
        self.assertIsNotNone(client_connection.http_client.base_url)
        self.assertEqual(client_connection.http_client.base_url, self.server_url)

        # Check api urls
        self.assertEqual(client_connection.api_url, api_url)
        self.assertEqual(client_connection.project_url, project_api_url)

# Executing the tests in the above test case class
if __name__ == "__main__":
    unittest.main()