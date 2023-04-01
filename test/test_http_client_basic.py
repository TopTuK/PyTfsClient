import pytest
from pytfsclient.services.http.http_client import HttpClient

### COMMAND 
# pytest .\test\test_http_client_basic.py
# https://stackoverflow.com/questions/5725430/http-test-server-accepting-get-post-requests

@pytest.fixture(scope="module")
def base_url() -> str:
    return 'https://httpbin.org/'

@pytest.fixture(scope="module")
def http_client(base_url: str) -> HttpClient:
    return HttpClient(base_url, verify=True)

@pytest.fixture(scope="module")
def get_action() -> str:
    return 'get'

@pytest.fixture(scope="module")
def post_action() -> str:
    return 'post'

@pytest.fixture(scope="module")
def patch_action() -> str:
    return 'patch'

# GET request test
def test_get_request_success(http_client: HttpClient, get_action: str):
    # Arrange

    # Act
    http_response = http_client.get(get_action)
    
    # Assert
    assert http_response, 'HTTP Response is None'
    assert http_response.content, 'HTTP Response content is None'
    
# GET Returns json response with args
def test_get_requests_args_success(http_client: HttpClient, get_action: str):
    # Arrange
    args = {
        "id": "1",
        "my_param": "my_value"
    }   

    # Act
    http_response = http_client.get(get_action, query_params=args)

    # Assert
    assert http_response, 'HTTP Response is None'
    assert http_response.content, 'HTTP Response content is None'

    content = http_response.json()
    assert content, 'Can\'t convert HTTP content to json'
    assert content['args'], 'HTTP Content args are None'

    assert content['args']['id'] == args['id']
    assert content['args']['my_param'] == args['my_param']

# POST request. Returns success response
def test_post_request_success(http_client: HttpClient, post_action: str):
    # Arrange 

    # Act
    http_response = http_client.post(post_action, None)

    # Assert
    assert http_response, 'HTTP Response is None'
    assert http_response.content, 'HTTP Response content is None'

# POST request. Returns json response with args
def test_post_request_args_success(http_client: HttpClient, post_action: str):
    # Arrange
    args = {
        "id": "1",
        "my_param": "my_value"
    }

    # Act
    http_response = http_client.post(post_action, args)

    # Assert
    assert http_response, 'HTTP Response is None'
    assert http_response.content, 'HTTP Response content is None'

    content = http_response.json()
    assert content, 'Can\'t convert HTTP content to json'
    assert content['form'], 'HTTP Content args are None'

    assert content['form']['id'] == args['id']
    assert content['form']['my_param'] == args['my_param']

# POST JSON request. Returns json response with args
def test_post_json_request_success(http_client: HttpClient, post_action: str):
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
    http_response = http_client.post_json(post_action, json_data=json)

    # Assert
    assert http_response, 'HTTP Response is None'
    assert http_response.content, 'HTTP Response content is None'

    content = http_response.json()
    assert content, 'Can\'t convert HTTP content to json'
    assert content['json'], 'HTTP json content does not have json elem'

    assert len(json) == len(content['json'])
    
# PATCH request Returns success response
def test_patch_request_success(http_client: HttpClient, patch_action: str):
    # Arrange

    # Act
    http_response = http_client.patch(patch_action, None)

    # Assert
    assert http_response, 'HTTP Response is None'
    assert http_response.content, 'HTTP Response content is None'

# patch JSON request. Returns json response with args
def test_patch_json_request_success(http_client: HttpClient, patch_action: str):
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
    http_response = http_client.patch_json(patch_action, json_data=json)

    # Assert
    assert http_response, 'HTTP Response is None'
    assert http_response.content, 'HTTP Response content is None'

    content = http_response.json()
    assert content, 'Can\'t convert HTTP content to json'
    assert content['json'], 'HTTP json content does not have json elem'

    assert len(json) == len(content['json'])