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
from pytfsclient.models.project.tfs_identity import Identity
from pytfsclient.models.project.tfs_team_member import TeamMember

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
def project_client(client_connection: ClientConnection) -> ProjectClient:
    return ClientFactory.get_project_client(client_connection)

def test_client_connection(client_connection: ClientConnection):
    assert client_connection, 'Client connection is None'

### MANAGING PROJECTS TESTS
def test_project_get_groups(project_client: ProjectClient):
    # Arrange
    identities = None

    # Act
    projects = project_client.get_projects()
    if projects and len(projects) > 0:
        project = projects[0]
        identities = project_client.get_project_groups(project)

    # Assert
    assert identities, 'Can\'t get project groups -> None'
    assert len(identities) > 0, 'Project groups list count is less than 1'
    for identity in identities:
        assert (identity.is_group or identity.is_user or identity.is_team), f'Identity type is not user or group. Type={identity.identity_type}'

def test_project_get_group_members(project_client: ProjectClient):
    # Arrange
    groups = None

    # Act
    projects = project_client.get_projects()
    if projects and len(projects) > 0:
        project = projects[0]
        identities = project_client.get_project_groups(project)

        if identities and len(identities) > 0:
            groups = dict()

            for identity in identities:
                if identity.is_group:
                    groups[identity] = project_client.get_project_group_members(project, identity)
                elif identity.is_team:
                    team = project_client.get_team(project.id, identity.foundation_id, True)
                    groups[identity] = project_client.get_project_team_members(project, team)
                else:
                    groups[identity] = identity

    # Assert
    assert groups, 'Can\'t get project group members -> None'
    
    for identity, value in groups.items():
        assert (identity.is_group or identity.is_user or identity.is_team), f'Identity type is not user or group. Type={identity.identity_type}'

        if identity.is_group:
            for member in value:
                assert (member.is_group or member.is_user or member.is_team), f'Member of group type is not user or group. Type={identity.identity_type}'

        if identity.is_team:
            assert len(value) > 0, 'List of team members is less 0'