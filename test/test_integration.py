import os, sys
# Manage paths
PROJECT_PATH = os.getcwd()
SOURCE_PATH = os.path.join(
    PROJECT_PATH, "src"
)
sys.path.append(SOURCE_PATH)

import pytest
import datetime
from pytfsclient.client_connection import ClientConnection
from pytfsclient.client_factory import ClientFactory
from pytfsclient.services.project_client.project_client import ProjectClient
from pytfsclient.services.workitem_client.workitem_client import WorkitemClient

### ^^^ ADDED EXTRA PATHS BELOW ^^^
### https://pytest-docs-ru.readthedocs.io/ru/latest/fixture.html

client_connection: ClientConnection = None

def setup_module(module):
    pat = os.environ['ENV_PAT']
    server_url = os.environ['ENV_SERVER_URL']
    project_name = os.environ['ENV_PROJECT_NAME']

    # Make global variable visible to 
    global client_connection

    client_connection = ClientFactory.create_pat(pat, server_url, project_name, verify_ssl=True)

@pytest.fixture(scope="module")
def workitem_client() -> WorkitemClient:
    return ClientFactory.get_workitem_client(client_connection)

def test_client_connection():
    assert client_connection, 'Client connection is None'

def test_get_workitem(workitem_client):
    # Arrange
    client: WorkitemClient = workitem_client
    workitem_title = '[BRQ] First test requirement'
    workitem_id = 1

    # Act
    wi = client.get_single_workitem(workitem_id)

    # Assert
    assert wi, 'Can\'t get workitem'
    assert wi.id == workitem_id, f'Workitem ID={wi.id} differs from requested ID={workitem_id}'
    assert wi.title == workitem_title

def test_create_workitem(workitem_client):
    # Arrange
    client: WorkitemClient = workitem_client
    
    today = datetime.date.today()
    wi_type_name = 'Requirement'
    wi_title = f'[BRQ] Created test requirement - {today}'
    wi_description = f'This BRQ was created by GitHub at {today}'

    wi_fields = {
        'System.Title': wi_title,
        'System.Description': wi_description,
    }

    # Act
    wi = client.create_workitem(wi_type_name, wi_fields)

    # Assert
    assert wi, 'Can\'t create Workitem!'
    assert wi.title == wi_title, 'Workitem title differs!'