from .http_client import HttpClient
from .tfs_client import API_VERSION, API_VERSION_PREVIEW, TfsBaseClient, TfsClientError
from .tfs_project_model import TeamMember, TfsProject, TfsTeam
from typing import List

_URL_PROJECTS = 'projects'
_URL_TEAMS = 'teams'
_URL_TEAM_MEMBERS = 'members'

class TfsProjectClient:
    def __init__(self, client: TfsBaseClient) -> None:
        self.__http: HttpClient = client.http_client
        self.__client: TfsBaseClient = client
    
    @property
    def client(self) -> TfsBaseClient:
        """
        :property: configured TfsBaseClient
        """
        return self.__client

    # https://docs.microsoft.com/en-us/rest/api/azure/devops/core/projects/list?view=azure-devops-rest-6.0
    def get_projects(self, skip: int = 0) -> List[TfsProject]:
        """
        Returns current list of Tfs projects 

        :param skip (int, optional): 
        :return: list of TfsProject
        """

        request_url = '{}/{}'.format(self.client.api_url, _URL_PROJECTS)
        query_params = {
            'api-version': API_VERSION,
            '$skip' : str(skip)
        }

        try:
            projects = list()
            
            hasNext = True
            while hasNext:
                response = self.__http.get(request_url, query_params=query_params)

                if not response:
                    raise TfsClientError('TfsClient::get_team_projects: can\'t get response from TFS server')
                
                json_items = response.json()
                if ('count' in json_items) and (int(json_items['count']) == 0):
                    hasNext = False
                    continue

                if 'value' in json_items:
                    json_items = json_items['value']
                    projects += [TfsProject.from_json(json_item) for json_item in json_items]
                    query_params['$skip'] = str(len(projects))
                else:
                    raise TfsClientError('TfsClient::get_team_projects: response doesn\'t have \'value\' attribute')
            
            return projects
        except Exception as ex:
            raise TfsClientError('TfsClient::get_team_projects: exception raised. Msg: {}'.format(ex), ex)

    # https://docs.microsoft.com/en-us/rest/api/azure/devops/core/teams/get-teams?view=azure-devops-rest-6.0
    def get_teams(self, current_user: bool = False) -> List[TfsTeam]:
        """
        Return list of TFS teams

        :param current_user (bool): If true return all the teams requesting user is member, otherwise return all the teams user has read access.
        :return: List of TfsTeam
        """

        request_url = '{}/{}'.format(self.client.api_url, _URL_TEAMS)
        query_params = {
            'api-version': API_VERSION_PREVIEW,
            '$mine' : str(current_user)
        }

        try:
            response = self.__http.get(request_url, query_params=query_params)
            if not response:
                raise TfsClientError('TfsClient::get_teams: can\'t get response from TFS server')

            json_items = response.json()
            if 'value' in json_items:
                json_items = json_items['value']
                return [TfsTeam.from_json(json_item) for json_item in json_items]
            else:
                raise TfsClientError('TfsClient::get_teams: response doesn\'t have \'value\' attribute')
        except Exception as ex:
            raise TfsClientError('TfsClient::get_teams: exception raised. Msg: {}'.format(ex), ex)

    # https://docs.microsoft.com/en-us/rest/api/azure/devops/core/teams/get-teams?view=azure-devops-rest-6.0
    def get_project_teams(self, project: TfsProject, expand: bool = False, current_user: bool = False, skip: int = 0) -> List[TfsTeam]:
        """
        Get a list of teams of project.

        :param: project (TfsProject): TFS project. Can't be None.
        :param: expand (bool): A value indicating whether or not to expand Identity information in the result WebApiTeam object.
        :param: current_user (bool): If true return all the teams requesting user is member, otherwise return all the teams user has read access.
        :param: skip (int): Default number of teams to skip.
        """
        assert project, 'TfsClient::get_project_teams: project can\'t be None'

        request_url = '{}/{}/{}/{}'.format(self.client.api_url, _URL_PROJECTS, project.id, _URL_TEAMS)
        query_params = {
            'api-version' : API_VERSION,
            '$expandIdentity' : str(expand),
            '$mine' : str(current_user),
            '$skip' : str(skip)
        }

        try:
            teams = list()

            hasNext = True
            while hasNext:
                response = self.__http.get(request_url, query_params=query_params)

                if not response:
                    raise TfsClientError('TfsClient::get_project_teams: can\'t get response from TFS server')

                json_items = response.json()
                if ('count' in json_items) and (int(json_items['count']) == 0):
                    hasNext = False
                    continue

                if 'value' in json_items:
                    json_items = json_items['value']
                    teams += [TfsTeam.from_json(json_item) for json_item in json_items]
                    query_params['$skip'] = str(len(teams))
                else:
                    raise TfsClientError('TfsClient::get_project_teams: response doesn\'t have \'value\' attribute')
            
            return teams
        except Exception as ex:
            raise TfsClientError('TfsClient::get_project_teams: exception raised. Msg: {}'.format(ex), ex)
    
    # https://docs.microsoft.com/en-us/rest/api/azure/devops/core/teams/get-team-members-with-extended-properties?view=azure-devops-rest-6.0
    def get_project_team_members(self, project: TfsProject, team: TfsTeam) -> List[TeamMember]:
        """
        Get a list of members for a specific team and a project.

        :param: project (TfsProject): The team project the team belongs to. Can't be None.
        :param: team (TfsTeam): specific team of project. Can't be None.
        :return: list of team members
        """
        assert project, 'TfsClient::get_project_team_members: project can\'t be None'
        assert team, 'TfsClient::get_project_team_members: team can\'t be None'

        request_url = '{}/{}/{}/{}/{}/{}'.format(self.client.api_url, _URL_PROJECTS, project.id, _URL_TEAMS, team.id, _URL_TEAM_MEMBERS)
        query_params = {
            'api-version' : API_VERSION,
            '$skip' : '0'
        }

        try:
            members = list()

            hasNext = True
            while hasNext:
                response = self.__http.get(request_url, query_params=query_params)

                if not response:
                    raise TfsClientError('TfsClient::get_project_team_members: can\'t get response from TFS server')

                json_items = response.json()
                if ('count' in json_items) and (int(json_items['count']) == 0):
                    hasNext = False
                    continue

                if 'value' in json_items:
                    json_items = json_items['value']
                    members += [TeamMember.from_json(json_item['identity']) for json_item in json_items]
                    query_params['$skip'] = str(len(members))
                else:
                    raise TfsClientError('TfsClient::get_project_team_members: response doesn\'t have \'value\' attribute')
            
            return members
        except Exception as ex:
            raise TfsClientError('TfsClient::get_project_team_members: exception raised. Msg: {}'.format(ex), ex)