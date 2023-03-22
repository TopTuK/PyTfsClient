from pytfsclient.models.project.tfs_project import TfsProject
from pytfsclient.models.project.tfs_team import TfsTeam
from pytfsclient.models.project.tfs_team_member import TfsTeamMemeber
from pytfsclient.services.base_client import BaseClient
from pytfsclient.services.client_connection import ClientConnection
from typing import List

class ProjectClient(BaseClient):
    """
    """

    # Constructor
    def __init__(self, client_connection: ClientConnection) -> None:
        super().__init__(client_connection)
    
    # https://docs.microsoft.com/en-us/rest/api/azure/devops/core/projects/list?view=azure-devops-rest-6.0
    def get_projects(self, skip: int = 0) -> List[TfsProject]:
        """
        """
        pass

    # https://docs.microsoft.com/en-us/rest/api/azure/devops/core/teams/get-teams?view=azure-devops-rest-6.0
    def get_all_teams(self, current_user: bool = False) -> List[TfsTeam]:
        """
        """
        pass

    # https://docs.microsoft.com/en-us/rest/api/azure/devops/core/teams/get-teams?view=azure-devops-rest-6.0
    def get_project_teams(self, project: TfsProject, expand: bool = False, current_user: bool = False, skip: int = 0) -> List[TfsTeam]:
        """
        """
        pass

    # https://docs.microsoft.com/en-us/rest/api/azure/devops/core/teams/get-team-members-with-extended-properties?view=azure-devops-rest-6.0
    def get_project_team_members(self, project: TfsProject, team: TfsTeam) -> List[TfsTeamMemeber]:
        """
        """
        pass