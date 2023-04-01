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
from pytfsclient.models.workitems.tfs_workitem_relation import WorkitemRelation, RelationTypes, RelationMap
from pytfsclient.models.workitems.tfs_workitem import UpdateFieldsResult

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

@pytest.fixture(scope="module")
def project_client() -> ProjectClient:
    return ClientFactory.get_project_client(client_connection)

def test_client_connection():
    assert client_connection, 'Client connection is None'

### MANAGING WORKITEMS TESTS

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

# TEST: Create new workitem. Type: Requirement
def test_create_workitem(workitem_client: WorkitemClient):
    # Arrange   
    today = datetime.date.today()
    wi_type_name = 'Requirement'
    wi_title = f'[BRQ] Created test requirement - {today}'
    wi_description = f'This BRQ was created by GitHub at {today}'

    wi_fields = {
        'System.Title': wi_title,
        'System.Description': wi_description,
    }

    # Act
    wi = workitem_client.create_workitem(wi_type_name, wi_fields)

    # Assert
    assert wi, 'Can\'t create Workitem!'
    assert wi.title == wi_title, 'Workitem title differs!'

def test_create_child_tasks(workitem_client: WorkitemClient):
    # Arrange
    today = datetime.date.today()

    parent_id = 2

    wi_type_name = 'Task'
    wi_title = f'[Task] Created by integration test - {today}'
    wi_description = f'This task was created by GitHub action at {today}'

    wi_fields = {
        'System.Title': wi_title,
        'System.Description': wi_description,
    }

    # Act
    parent = workitem_client.get_single_workitem(parent_id)
    relations = [
        WorkitemRelation.create(RelationMap[RelationTypes.PARENT], parent)
    ]

    wi = workitem_client.create_workitem(wi_type_name, wi_fields, relations)

    # Assert
    assert wi, 'Can\'t create Workitem!'
    assert wi.title == wi_title, 'Workitem title differs!'

    assert wi.relations, 'Workitem relations are None'
    assert len(relations) == len(wi.relations), 'Workitem relations count is not same!'

    # Check onlu one relation
    assert wi.relations[0].destination_id == relations[0].destination_id

def test_update_workitem_fields(workitem_client: WorkitemClient):
    # Arrange
    today = datetime.date.today()
    workitem_id = 2

    title = f'[BRQ] Modified test requirement {today}'
    description = f'This BRQ was modified by GitHub action. Last update: {today}'
    history = f'GitHub action was starter {today}'

    # Act
    wi = workitem_client.get_single_workitem(workitem_id)
    wi.title = title
    wi['System.Description'] = description
    wi['System.History'] = history

    update_result = wi.update_fields()

    wi_compare = workitem_client.get_single_workitem(workitem_id)

    # Assert
    assert update_result == UpdateFieldsResult.UPDATE_SUCCESS, f'Update error: {update_result}'
    assert wi.title == title, 'Can\'t modify Title'

    assert wi.id == wi_compare.id
    assert wi.title == wi_compare.title, 'Can\'t save changes'
    assert wi.description == wi_compare['System.Description']

### END OF WORKITEMS TESTS

### MANAGING PROJECTS TESTS
def test__project_client(project_client: ProjectClient):
    # Arrange

    # Act
    projects = project_client.get_projects()
    teams = project_client.get_all_teams()

    prj_teams = None
    members = None
    if projects and len(projects) > 0:
        prj_teams = project_client.get_project_teams(projects[0])

        if prj_teams and len(prj_teams) > 0:
            members = project_client.get_project_team_members(project=projects[0], team=prj_teams[0])

    # Assert
    assert projects, 'Can\'t get projects -> None'
    assert len(projects) < 1, 'Projects list count is less than 1'

    assert teams, 'Can\'t get teams'
    assert len(teams) < 1, 'Teams list count is less than 1'

    assert prj_teams, f'Can\'t get project teams. Project: {projects[0].id} {projects[0].name}'

    assert members, f'Can\'t get members of {prj_teams[0].id} {prj_teams[0].name} for {projects[0].id} {projects[0].name}'
    assert len(members) < 1, 'Members list count is less than 1'

### END OF MANAGING PROJECTS TESTS