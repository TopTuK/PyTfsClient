from pytfsclient.models.client_error import ClientError
from pytfsclient.models.project.tfs_project import TfsProject
from pytfsclient.models.project.tfs_team import TfsTeam
from pytfsclient.models.project.tfs_team_member import TfsTeamMember
from pytfsclient.services.base_client import BaseClient
from pytfsclient.services.client_connection import ClientConnection
from typing import List

class ProjectClient(BaseClient):
    """
    Tfs ProjectClient facade for managing projects, teams and team members
    """

    _URL_PROJECTS = 'projects'
    _URL_TEAMS = 'teams'
    _URL_TEAM_MEMBERS = 'members'

    # Constructor
    def __init__(self, client_connection: ClientConnection) -> None:
        super().__init__(client_connection)
    
    # https://docs.microsoft.com/en-us/rest/api/azure/devops/core/projects/list?view=azure-devops-rest-6.0
    def get_projects(self, skip: int = 0) -> List[TfsProject]:
        """
        Returns current list of Tfs projects 
        """
        
        request_url = f'{self.client_connection.api_url}{self._URL_PROJECTS}'
        query_params = {
            'api-version': self.api_version,
            '$skip' : str(skip)
        }

        try:
            projects = list()

            hasNext = True
            while hasNext:
                response = self.http_client.get(request_url, query_params=query_params)

                if not response:
                    raise ClientError('ProjectClient::get_projects: can\'t get response from TFS server')

                json_items = response.json()
                if ('count' in json_items) and (int(json_items['count']) == 0):
                    hasNext = False
                    continue

                if 'value' in json_items:
                    json_items = json_items['value']
                    projects += [TfsProject.from_json(json_item) for json_item in json_items]
                    query_params['$skip'] = str(len(projects))
                else:
                    raise ClientError('ProjectClient::get_projects: response doesn\'t have \'value\' attribute')
            
            return projects
        except Exception as ex:
            raise ClientError(f'ProjectClient::get_projects: exception raised. Msg: {ex}', ex)

    # https://docs.microsoft.com/en-us/rest/api/azure/devops/core/teams/get-teams?view=azure-devops-rest-6.0
    def get_all_teams(self, current_user: bool = False) -> List[TfsTeam]:
        """
        Return list of TFS teams
        """

        request_url = f'{self.client_connection.api_url}{self._URL_TEAMS}'
        query_params = {
            'api-version': self.api_version_preview,
            '$mine' : str(current_user)
        }

        try:
            response = self.http_client.get(request_url, query_params=query_params)

            if not response:
                raise ClientError('ProjectClient::get_all_teams: can\'t get response from TFS server')
            
            json_items = response.json()
            if 'value' in json_items:
                json_items = json_items['value']
                return [TfsTeam.from_json(json_item) for json_item in json_items]
            else:
                raise ClientError('ProjectClient::get_all_teams: response doesn\'t have \'value\' attribute')
        except Exception as ex:
            raise ClientError(f'ProjectClient::get_all_teams: exception raised. Msg: {ex}', ex)

    # https://docs.microsoft.com/en-us/rest/api/azure/devops/core/teams/get-teams?view=azure-devops-rest-6.0
    def get_project_teams(self, project: TfsProject, expand: bool = False, \
                          current_user: bool = False, skip: int = 0) -> List[TfsTeam]:
        """
        Get a list of teams of project.
        """

        assert project, 'ProjectClient::get_project_teams: project can\'t be None'

        request_url = f'{self.client_connection.api_url}{self._URL_PROJECTS}/{project.id}/{self._URL_TEAMS}'
        query_params = {
            'api-version' : self.api_version,
            '$expandIdentity' : str(expand),
            '$mine' : str(current_user),
            '$skip' : str(skip)
        }

        try:
            teams = list()

            hasNext = True
            while hasNext:
                response = self.http_client.get(request_url, query_params=query_params)

                if not response:
                    raise ClientError('ProjectClient::get_project_teams: can\'t get response from TFS server')
        
                json_items = response.json()
                if ('count' in json_items) and (int(json_items['count']) == 0):
                    hasNext = False
                    continue

                if 'value' in json_items:
                    json_items = json_items['value']
                    teams += [TfsTeam.from_json(json_item) for json_item in json_items]
                    query_params['$skip'] = str(len(teams))
                else:
                    raise ClientError('ProjectClient::get_project_teams: response doesn\'t have \'value\' attribute')
                
            return teams
        except Exception as ex:
            raise ClientError(f'ProjectClient::get_project_teams: exception raised. Msg: {ex}', ex)
        
    # https://docs.microsoft.com/en-us/rest/api/azure/devops/core/teams/get-team-members-with-extended-properties?view=azure-devops-rest-6.0
    def get_project_team_members(self, project: TfsProject, team: TfsTeam) -> List[TfsTeamMember]:
        """
        Get a list of members for a specific team and a project.
        """
        
        assert project, 'ProjectClient::get_project_team_members: project can\'t be None'
        assert team, 'ProjectClient::get_project_team_members: team can\'t be None'

        request_url = f'{self.client_connection.api_url}{self._URL_PROJECTS}/{project.id}/{self._URL_TEAMS}/{team.id}/{self._URL_TEAM_MEMBERS}'
        query_params = {
            'api-version' : self.api_version,
            '$skip' : '0'
        }

        try:
            members = list()

            hasNext = True
            while hasNext:
                response = self.http_client.get(request_url, query_params=query_params)

                if not response:
                        raise ClientError('ProjectClient::get_project_team_members: can\'t get response from TFS server')    
                
                json_items = response.json()
                if ('count' in json_items) and (int(json_items['count']) == 0):
                        hasNext = False
                        continue
                
                if 'value' in json_items:
                    json_items = json_items['value']
                    members += [TfsTeamMember.from_json(json_item['identity']) for json_item in json_items]
                    query_params['$skip'] = str(len(members))
                else:
                    raise ClientError('ProjectClient::get_project_team_members: response doesn\'t have \'value\' attribute')
                
            return members
        except Exception as ex:
            raise ClientError(f'ProjectClient::get_project_team_members: exception raised. Msg: {ex}', ex)

    # https://docs.microsoft.com/en-us/rest/api/azure/devops/core/teams/get-teams?view=azure-devops-rest-6.0
    def get_project_teams(self, project: TfsProject, expand: bool = False, \
                          current_user: bool = False, skip: int = 0) -> List[TfsTeam]:
        """
        Get a list of members for a specific team and a project
        """

        assert project, 'ProjectClient::get_project_teams: project can\'t be None'

        request_url = f'{self.client_connection.api_url}{self._URL_PROJECTS}/{project.id}/{self._URL_TEAMS}'
        query_params = {
            'api-version' : self.api_version,
            '$expandIdentity' : str(expand),
            '$mine' : str(current_user),
            '$skip' : str(skip)
        }

        try:
            teams = list()

            hasNext = True
            while hasNext:
                response = self.http_client.get(request_url, query_params=query_params)

                if not response:
                    raise ClientError('ProjectClient::get_project_teams: can\'t get response from TFS server')
                
                json_items = response.json()
                if ('count' in json_items) and (int(json_items['count']) == 0):
                    hasNext = False
                    continue

                if 'value' in json_items:
                    json_items = json_items['value']
                    teams += [TfsTeam.from_json(json_item) for json_item in json_items]
                    query_params['$skip'] = str(len(teams))
                else:
                    raise ClientError('ProjectClient::get_project_teams: response doesn\'t have \'value\' attribute')
            
            return teams
        except Exception as ex:
            raise ClientError(f'ProjectClient::get_project_teams: exception raised. Msg: {ex}', ex)

    # https://docs.microsoft.com/en-us/rest/api/azure/devops/core/teams/get-team-members-with-extended-properties?view=azure-devops-rest-6.0
    def get_project_team_members(self, project: TfsProject, team: TfsTeam) -> List[TfsTeamMember]:
        """
        Get a list of members for a specific team and a project.
        """
        
        assert project, 'ProjectClient::get_project_team_members: project can\'t be None'
        assert team, 'ProjectClient::get_project_team_members: team can\'t be None'

        request_url = f'{self.client_connection.api_url}{self._URL_PROJECTS}/{project.id}/{self._URL_TEAMS}/{team.id}/{self._URL_TEAM_MEMBERS}'
        query_params = {
            'api-version' : self.api_version,
            '$skip' : '0'
        }

        try:
            members = list()

            hasNext = True
            while hasNext:
                response = self.http_client.get(request_url, query_params=query_params)

                if not response:
                    raise ClientError('ProjectClient::get_project_team_members: can\'t get response from TFS server')
                
                json_items = response.json()
                if ('count' in json_items) and (int(json_items['count']) == 0):
                    hasNext = False
                    continue

                if 'value' in json_items:
                    json_items = json_items['value']
                    members += [TfsTeamMember.from_json(json_item['identity']) for json_item in json_items]
                    query_params['$skip'] = str(len(members))
                else:
                    raise ClientError('ProjectClient::get_project_team_members: response doesn\'t have \'value\' attribute')

            return members
        except Exception as ex:
            raise ClientError(f'ProjectClient::get_project_team_members: exception raised. Msg: {ex}', ex)
