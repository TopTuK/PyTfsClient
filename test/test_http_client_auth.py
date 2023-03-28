import context
import unittest
import warnings
from pytfsclient.services.http.http_client import HttpClient

class HttpClientAuthTests(unittest.TestCase):

    def setUp(self):
        warnings.simplefilter('ignore', category=ResourceWarning)

        self.base_url = 'https://httpbin.org/'
        self.http_client: HttpClient = HttpClient(self.base_url, verify=True)

    # AUTH Returns successful auth
    @unittest.skip("NTLM AUTH is not supported via httpbin")
    def test_http_auth_success(self):
        
        # Arrange
        user_name = 'user'
        user_password = 'pwd'

        request_url = f'basic-auth/{user_name}/{user_password}'

        # Act
        self.http_client.authentificate_with_password(user_name, user_password)
        http_response = self.http_client.get(request_url)

        # Assert
        self.assertIsNotNone(http_response, 'HTTP Response is None')
        self.assertIsNotNone(http_response.content, 'HTTP Response content is None')
    
    # COOKIE set get Returns success if set and get cookies
    def test_cookie_set_get(self):
        
        # Arrange
        cookie_value = "myCookieValue"

        cookies = dict(myCookie=cookie_value)

        request_url = "cookies"

        # Act
        http_response = self.http_client.get(request_url, cookies=cookies)

        # Assert
        self.assertIsNotNone(http_response, 'HTTP Response is None')
        self.assertIsNotNone(http_response.cookies, 'HTTP Response does not have cookies')

# Executing the tests in the above test case class
if __name__ == "__main__":
    unittest.main()