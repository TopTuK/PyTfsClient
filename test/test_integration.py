import os, sys
# Manage paths
PROJECT_PATH = os.getcwd()
SOURCE_PATH = os.path.join(
    PROJECT_PATH, "src"
)
sys.path.append(SOURCE_PATH)

import pytest
from pytfsclient.client_connection import ClientConnection
from pytfsclient.client_factory import ClientFactory
from pytfsclient.services.project_client.project_client import ProjectClient
from pytfsclient.services.workitem_client.workitem_client import WorkitemClient

### ^^^ ADDED EXTRA PATHS BELOW ^^^

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
    client: WorkitemClient = workitem_client
    
    workitem_id = 14
    wi = client.get_single_workitem(workitem_id)

    assert wi, 'Can\'t get workitem'
    assert wi.id == workitem_id, f'Workitem ID={wi.id} differs from requested ID={workitem_id}'
