import pytest
from pytfsclient.client_factory import ClientFactory

### Command
# pytest .\test\test_client_connection2.py

def test_create_client_connection():
    # Arrange
    server_url = 'http://localhost/'
    collection = 'DefaultCollection'
    project = 'TestProject'

    project_name = f'{collection}/{project}'
    fake_pat = 'fakepat'

    api_url = f'{collection}/_apis/'
    project_api_url = f'{collection}/{project}/_apis/'

    # Act
    client_connection = ClientFactory.create_pat(fake_pat, server_url, project_name)

    # Assert
    assert client_connection.server_url == server_url
    assert client_connection.collection == collection
    assert client_connection.project_name == project

    # Check server url
    assert client_connection.http_client
    assert client_connection.http_client.base_url
    assert client_connection.http_client.base_url == server_url

    # Check api urls
    assert client_connection.api_url == api_url
    assert client_connection.project_url == project_api_url