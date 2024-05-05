import os
import datetime
import pytest
from pytfsclient.tfs_client_factory import TfsClientFactory
from pytfsclient.tfs_client import TfsBaseClient
from pytfsclient.tfs_project_client import TfsProjectClient
from pytfsclient.tfs_workitem_client import TfsWorkitemClient
from pytfsclient.tfs_workitem_model import TfsWorkitem, TfsUpdateFieldsResult
from pytfsclient.tfs_workitem_relation_model import TfsWorkitemRelation, RelationTypes, RelationMap

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
def base_client(server_url, project_name, personal_access_token) -> TfsBaseClient:
    client = TfsClientFactory.create(server_url, project_name, True)
    client.authentificate_with_pat(personal_access_token)

    return client

@pytest.fixture(scope="module")
def workitem_client(base_client) -> TfsWorkitemClient:
    client = TfsClientFactory.get_workitem_client(base_client)

    return client

@pytest.fixture(scope="module")
def project_client(base_client) -> TfsProjectClient:
    client = TfsClientFactory.get_project_client(base_client)

    return client

### MANAGING WORKITEMS TESTS
@pytest.mark.skip(reason="SKIP by now")
def test_get_workitem(workitem_client: TfsWorkitemClient):
    # Arrange
    workitem_title = '[BRQ] First test requirement'
    workitem_id = 1

    # Act
    wi = workitem_client.get_single_workitem(workitem_id)

    # Assert
    assert wi, 'Can\'t get workitem'
    assert isinstance(wi, TfsWorkitem), 'Workitem is not instance of TfsWorkitem'
    assert wi.id == workitem_id, f'Workitem ID={wi.id} differs from requested ID={workitem_id}'
    assert wi.title == workitem_title

# TEST: Create new workitem. Type: Requirement
@pytest.mark.skip(reason="SKIP by now")
def test_create_workitem(workitem_client: TfsWorkitemClient):
    # Arrange   
    today = datetime.date.today()
    wi_type_name = 'Requirement'
    wi_title = f'[BRQ] Created backwared test requirement - {today}'
    wi_description = f'This BRQ was created by GitHub at {today}'

    wi_fields = [{
        'System.Title': wi_title,
        'System.Description': wi_description,
    }]

    # Act
    wi = workitem_client.create_workitem(wi_type_name, wi_fields)

    # Assert
    assert wi, 'Can\'t create Workitem!'
    assert isinstance(wi, TfsWorkitem), 'Workitem is not instance of TfsWorkitem'
    assert wi.title == wi_title, 'Workitem title differs!'

@pytest.mark.skip(reason="SKIP by now")
def test_create_child_tasks(workitem_client: TfsWorkitemClient):
    # Arrange
    today = datetime.date.today()

    parent_id = 2

    wi_type_name = 'Task'
    wi_title = f'[Task] Created by backwared test - {today}'
    wi_description = f'This task was created by GitHub action at {today}'

    wi_fields = [{
        'System.Title': wi_title,
        'System.Description': wi_description,
    }]

    # Act
    parent = workitem_client.get_single_workitem(parent_id)
    relations = [
        TfsWorkitemRelation.create(RelationMap[RelationTypes.PARENT], parent)
    ]

    wi = workitem_client.create_workitem(wi_type_name, wi_fields, relations)

    # Assert
    assert wi, 'Can\'t create Workitem!'
    assert wi.title == wi_title, 'Workitem title differs!'

    assert wi.relations, 'Workitem relations are None'
    assert len(relations) == len(wi.relations), 'Workitem relations count is not same!'

    # Check only one relation
    assert wi.relations[0].destination_id == relations[0].destination_id

@pytest.mark.skip(reason="SKIP by now")
def test_update_workitem_fields(workitem_client: TfsWorkitemClient):
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
    assert update_result == TfsUpdateFieldsResult.UPDATE_SUCCESS, f'Update error: {update_result}'
    assert wi.title == title, 'Can\'t modify Title'

    assert wi.id == wi_compare.id
    assert wi.title == wi_compare.title, 'Can\'t save changes'
    assert wi.description == wi_compare['System.Description']

### END OF MANAGING WORKITEMS TESTS

### MANAGING PROJECTS TESTS
@pytest.mark.skip(reason="SKIP by now")
def test__project_client(project_client: TfsProjectClient):
    # Arrange

    # Act
    projects = project_client.get_projects()
    teams = project_client.get_teams()

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