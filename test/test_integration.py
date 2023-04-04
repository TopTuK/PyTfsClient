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
from pytfsclient.models.workitems.tfs_workitem_changes import WorkitemChange, FieldChange, WorkitemRelationChanges
from pytfsclient.models.project.tfs_team_member import TfsTeamMember

### ^^^ ADDED EXTRA PATHS BELOW ^^^
### https://pytest-docs-ru.readthedocs.io/ru/latest/fixture.html

@pytest.fixture(scope="module")
def server_url() -> str:
    return os.environ['ENV_SERVER_URL']

@pytest.fixture(scope="module")
def project_name() -> str:
    return os.environ['ENV_PROJECT_NAME']

@pytest.fixture(scope="module")
def personal_access_token() -> str:
    return os.environ['ENV_PAT']

@pytest.fixture(scope="module")
def client_connection(server_url, project_name, personal_access_token) -> ClientConnection:
    client_connection = ClientFactory.create_pat(personal_access_token, server_url, project_name, True)

    return client_connection

@pytest.fixture(scope="module")
def workitem_client(client_connection: ClientConnection) -> WorkitemClient:
    return ClientFactory.get_workitem_client(client_connection)

@pytest.fixture(scope="module")
def project_client(client_connection: ClientConnection) -> ProjectClient:
    return ClientFactory.get_project_client(client_connection)

def test_client_connection(client_connection: ClientConnection):
    assert client_connection, 'Client connection is None'

### MANAGING WORKITEMS TESTS

def test_get_workitem(workitem_client: WorkitemClient):
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

def test_get_worktime_changes(workitem_client: WorkitemClient):
    # Arrange
    workitem_id = 6 # [BRQ] Python requirement edited

    # Act
    changes = workitem_client.get_workitem_changes(workitem_id)

    # Asset
    assert changes, 'Workitem changes are None'
    assert len(changes) > 0, 'Workitem changes are empty'

    for change in changes:
        assert change.id, 'Workitem change is None'
        assert change.revision, 'Workitem revision is None'

        if change.field_changes:
            assert len(change.field_changes) > 0, ''

            for fld_change in change.field_changes:
                assert fld_change.name, 'Field change name is None'
                assert fld_change.new_value, f'Field {fld_change.name} change does not have new value'

        if change.relation_changes:
            rel_changes = change.relation_changes

            assert rel_changes.added or rel_changes.removed or rel_changes.updated, 'Workitem doesn\'t have relation changes'

            if rel_changes.added:
                for rel in rel_changes.added:
                    assert rel.relation_name, 'Added relation doesn\'t have relation name'
                    assert rel.destination_id, 'Added relation doesn\'t have destination id'

            if rel_changes.removed:
                for rel in rel_changes.removed:
                    assert rel.relation_name, 'Removed relation doesn\'t have relation name'
                    assert rel.destination_id, 'Removed relation doesn\'t have destination id'

            if rel_changes.updated:
                for rel in rel_changes.updated:
                    assert rel.relation_name, 'Updated relation doesn\'t have relation name'
                    assert rel.destination_id, 'Updated relation doesn\'t have destination id'

### END OF WORKITEMS TESTS

### MANAGING PROJECTS TESTS
def test_project_client(project_client: ProjectClient):
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
    assert len(projects) > 0, 'Projects list count is less than 1'

    assert teams, 'Can\'t get teams'
    assert len(teams) > 0, 'Teams list count is less than 1'

    assert prj_teams, f'Can\'t get project teams. Project: {projects[0].id} {projects[0].name}'

    assert members, f'Can\'t get members of {prj_teams[0].id} {prj_teams[0].name} for {projects[0].id} {projects[0].name}'
    assert len(members) > 0, 'Members list count is less than 1'

### END OF MANAGING PROJECTS TESTS