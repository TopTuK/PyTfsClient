import pytest
from pytfsclient.services.http.http_client import HttpClient

### COMMAND
#  pytest .\test\test_http_client_auth.py

@pytest.fixture(scope="module")
def base_url() -> str:
    return 'https://httpbin.org/'

@pytest.fixture(scope="module")
def http_client(base_url) -> HttpClient:
    return HttpClient(base_url, verify=True)

# AUTH Returns successful auth
@pytest.mark.skip(reason="NTLM AUTH is not supported via httpbin")
def test_http_auth_success(http_client: HttpClient):
    # Arrange
    user_name = 'user'
    user_password = 'pwd'

    request_url = f'basic-auth/{user_name}/{user_password}'

    # Act
    http_client.authentificate_with_password(user_name, user_password)
    http_response = http_client.get(request_url)

    # Assert
    assert http_response, 'HTTP Response is None'
    assert http_response.content, 'HTTP Response content is None'

# COOKIE set get Returns success if set and get cookies
def test_cookie_set_get(http_client: HttpClient):
    # Arrange
    cookie_value = "myCookieValue"
    cookies = dict(myCookie=cookie_value)

    request_url = "cookies"

    # Act
    http_response = http_client.get(request_url, cookies=cookies)

    # Assert
    assert http_response, 'HTTP Response is None'
    # assert http_response.cookies, 'HTTP Response does not have cookies'