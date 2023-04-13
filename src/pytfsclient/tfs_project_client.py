from .tfs_client import TfsBaseClient, TfsClientError
from .tfs_project_model import TeamMember, TfsProject, TfsTeam
from typing import List

from .client_factory import ClientFactory
from .services.project_client.project_client import ProjectClient
from .models.project.tfs_project import Project as TProject
from .models.project.tfs_team import Team as TTeam

### DEPRECATED IN NEXT VERSIONS ####

class TfsProjectClient:
    def __init__(self, client: TfsBaseClient) -> None:
        self.__client: TfsBaseClient = client
        self.__prj_client: ProjectClient = ClientFactory.get_project_client(client.client_connection)
    
    @property
    def client(self) -> TfsBaseClient:
        """
        :property: configured TfsBaseClient
        """
        return self.__client

    def get_projects(self, skip: int = 0) -> List[TfsProject]:
        """
        Returns current list of Tfs projects 

        :param skip (int, optional): 
        :return: list of TfsProject
        """

        try:
            projects = self.__prj_client.get_projects()
            return [TfsProject.create(project.id, project.name, project.url) for project in projects]
        except Exception as ex:
            raise TfsClientError('TfsClient::get_team_projects: exception raised. Msg: {}'.format(ex), ex)

    def get_teams(self, current_user: bool = False) -> List[TfsTeam]:
        """
        Return list of TFS teams

        :param current_user (bool): If true return all the teams requesting user is member, otherwise return all the teams user has read access.
        :return: List of TfsTeam
        """

        try:
            teams = self.__prj_client.get_all_teams(current_user=current_user)
            return [TfsTeam.create(team.id, team.name, team.url) for team in teams]
        except Exception as ex:
            raise TfsClientError('TfsClient::get_teams: exception raised. Msg: {}'.format(ex), ex)

    def get_project_teams(self, project: TfsProject, expand: bool = False, current_user: bool = False, skip: int = 0) -> List[TfsTeam]:
        """
        Get a list of teams of project.

        :param: project (TfsProject): TFS project. Can't be None.
        :param: expand (bool): A value indicating whether or not to expand Identity information in the result WebApiTeam object.
        :param: current_user (bool): If true return all the teams requesting user is member, otherwise return all the teams user has read access.
        :param: skip (int): Default number of teams to skip.
        """
        assert project, 'TfsClient::get_project_teams: project can\'t be None'

        try:
            prj = TProject.create(project.id, project.name, url=project.url)
            teams = self.__prj_client.get_project_teams(prj, expand, current_user, skip)

            return [TfsTeam.create(team.id, team.name, team.url) for team in teams]
        except Exception as ex:
            raise TfsClientError('TfsClient::get_project_teams: exception raised. Msg: {}'.format(ex), ex)
    
    def get_project_team_members(self, project: TfsProject, team: TfsTeam) -> List[TeamMember]:
        """
        Get a list of members for a specific team and a project.

        :param: project (TfsProject): The team project the team belongs to. Can't be None.
        :param: team (TfsTeam): specific team of project. Can't be None.
        :return: list of team members
        """
        assert project, 'TfsClient::get_project_team_members: project can\'t be None'
        assert team, 'TfsClient::get_project_team_members: team can\'t be None'

        try:
           internal_prj = TProject.create(project.id, project.name, project.url)
           internal_team = TTeam.create(team.id, team.name, team.url)

           members = self.__prj_client.get_project_team_members(internal_prj, internal_team)

           return [TeamMember.create(member.id, member.display_name, member.unique_name, member.url) for member in members]
        except Exception as ex:
            raise TfsClientError('TfsClient::get_project_team_members: exception raised. Msg: {}'.format(ex), ex)