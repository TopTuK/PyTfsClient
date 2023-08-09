from ...models.client_error import ClientError
from ...models.project.tfs_project import Project
from ...models.project.tfs_team import Team
from ...models.project.tfs_identity import Identity
from ...models.project.tfs_team_member import TeamMember
from ...services.base_client import BaseClient
from ...client_connection import ClientConnection
from typing import List

class ProjectClient(BaseClient):
    '''
    ProjectClient facade for managing projects, teams and team members
    '''

    _URL_PROJECTS = 'projects'
    _URL_TEAMS = 'teams'
    _URL_TEAM_MEMBERS = 'members'

    # Constructor
    def __init__(self, client_connection: ClientConnection) -> None:
        super().__init__(client_connection)
    
    def get_projects(self, skip: int = 0) -> List[Project]:
        '''
        Returns current list of Tfs/Azure projects.
        Docs: https://docs.microsoft.com/en-us/rest/api/azure/devops/core/projects/list?view=azure-devops-rest-6.0

        Args:
            skip (int): number top project to skip. Default: 0

        Returns:
            List of project: List[Project]
        
        Raises:
            ClientError with information about exception
        '''
        
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
                    projects += [Project.from_json(json_item) for json_item in json_items]
                    query_params['$skip'] = str(len(projects))
                else:
                    raise ClientError('ProjectClient::get_projects: response doesn\'t have \'value\' attribute')
            
            return projects
        except Exception as ex:
            raise ClientError(f'ProjectClient::get_projects: exception raised. Msg: {ex}', ex)

    def get_project(self, project_id: str, capabilities: bool = False, history: bool = False) -> Project:
        '''
        Returns TFS/Azure project instance.
        Docs: https://learn.microsoft.com/en-us/rest/api/azure/devops/core/projects/get?view=azure-devops-rest-6.0

        Args:
            project_id (str): project id. Can't be None.
            capabilities (bool): Include capabilities (such as source control) in the team project result (default: false).
            history (bool): Search within renamed projects (that had such name in the past).

        Returns:
            Project instance.
        
        Raises:
            ClientError with information about exception
        '''

        if not project_id:
            raise ClientError('ProjectClient::get_project: project id can\'t be None')

        request_url = f'{self.client_connection.api_url}{self._URL_PROJECTS}/{project_id}'
        query_params = {
            'api-version': self.api_version,
            'includeCapabilities' : str(capabilities),
            'includeHistory' : str(history)
        }

        try:
            response = self.http_client.get(request_url, query_params=query_params)

            if not response:
                raise ClientError('ProjectClient::get_project: can\'t get response from TFS server')
            
            json_item = response.json()
            return Project.from_json(json_item)
        except Exception as ex:
            raise ClientError(f'ProjectClient::get_project: exception raised. Msg: {ex}', ex)
        
    def get_team(self, project_id: str, team_id: str, expand: bool = False) -> Team:
        '''
        Returns TFS/Azure team instance.
        Docs: https://learn.microsoft.com/en-us/rest/api/azure/devops/core/teams/get?view=azure-devops-rest-6.0&tabs=HTTP

        Args:
            project_id (str): project id. Can't be None.
            team_id (str): team id. Can't be None.
            expand (bool): A value indicating whether or not to expand Identity information in the result WebApiTeam object.

        Returns:
            Team instance.
        
        Raises:
            ClientError with information about exception
        '''

        if not project_id:
            raise ClientError('ProjectClient::get_project: project id can\'t be None')
        if not team_id:
            raise ClientError('ProjectClient::get_project: team id can\'t be None')
        
        request_url = f'{self.client_connection.api_url}{self._URL_PROJECTS}/{project_id}/{self._URL_TEAMS}/{team_id}'
        query_params = {
            'api-version': self.api_version,
            '$expandIdentity' : str(expand)
        }
        try:
            response = self.http_client.get(request_url, query_params=query_params)

            if not response:
                raise ClientError('ProjectClient::get_project: can\'t get response from TFS server')
            
            json_item = response.json()
            return Team.from_json(json_item)
        except Exception as ex:
            raise ClientError(f'ProjectClient::get_project: exception raised. Msg: {ex}', ex)

    def get_all_teams(self, current_user: bool = False) -> List[Team]:
        '''
        Returns list of TFS/Azure teams.
        Docs: https://docs.microsoft.com/en-us/rest/api/azure/devops/core/teams/get-teams?view=azure-devops-rest-6.0

        Args:
            current_user (bool): If true return all the teams requesting user is member, otherwise return all the teams user has read access.
        
        Returns:
            List of TFS/Azure teams: List[Team]
        
        Raises:
            ClientError with information about exception
        '''

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
                return [Team.from_json(json_item) for json_item in json_items]
            else:
                raise ClientError('ProjectClient::get_all_teams: response doesn\'t have \'value\' attribute')
        except Exception as ex:
            raise ClientError(f'ProjectClient::get_all_teams: exception raised. Msg: {ex}', ex)
    
    def get_project_groups(self, project: Project) -> List[Identity]:
        '''
        Get a list of identities for the project
        Non-public api: {project_id}/_api/_identity/ReadScopedApplicationGroupsJson?__v=5

        Args:
            project (Project): project instance. Can't be None
        
        Returns:
            List of project identities: List[Identity]
        
        Raises:
            ClientError if identities is None or bad request
        '''

        if not project:
            raise ClientError('ProjectClient::get_project_groups: project can\'t be None')

        request_url = f'{self.client_connection.collection}/{project.id}/_api/_identity/ReadScopedApplicationGroupsJson'
        query_params = {
            '__v' : 5,
        }

        try:
            response = self.http_client.get(request_url, query_params=query_params)

            if not response:
                raise ClientError('ProjectClient::get_project_groups: can\'t get response from TFS server')
            
            json_items = response.json()
            if 'identities' in json_items:
                return [Identity.from_json(json_item) for json_item in json_items['identities']]
            else:
                return []
        except Exception as ex:
            raise ClientError(f'ProjectClient::get_project_groups: exception raised. Msg: {ex}', ex)
    
    def get_project_group_members(self, project: Project, identity: Identity) -> List[Identity]:
        '''
        Get a list of project group members
        Non-public api: {project_id}/_api/_identity/ReadGroupMembers?__v=5&scope={group.foundation_id}&readMembers=true

        Args:
            project (Project): project instance. Can't be None
            identity (Identity): identity of project. Can'be None and should be group
        
        Returns:
            List of project identities: List[Identity]
        
        Raises:
            ClientError if identities is None or bad request
        '''

        if not project:
            raise ClientError('ProjectClient::get_project_group_members: project can\'t be None')
        
        if not identity:
            raise ClientError('ProjectClient::get_project_group_members: identity can\'t be None')
        if not identity.is_group:
            raise ClientError('ProjectClient::get_project_group_members: identity should be group')

        request_url = f'{self.client_connection.collection}/{project.id}/_api/_identity/ReadGroupMembers'
        query_params = {
            '__v' : 5,
            'scope' : identity.foundation_id,
            'readMembers' : 'true',
        }

        try:
            response = self.http_client.get(request_url, query_params=query_params)

            if not response:
                raise ClientError('ProjectClient::get_project_group_members: can\'t get response from TFS server')
            
            json_items = response.json()
            if 'identities' in json_items:
                return [Identity.from_json(json_item) for json_item in json_items['identities']]
            else:
                return []
        except Exception as ex:
            raise ClientError(f'ProjectClient::get_project_group_members: exception raised. Msg: {ex}', ex)

    def get_project_teams(self, project: Project, expand: bool = False, \
                          current_user: bool = False, skip: int = 0) -> List[Team]:
        '''
        Get a list of members for a specific team and a project.
        Docs: https://docs.microsoft.com/en-us/rest/api/azure/devops/core/teams/get-teams?view=azure-devops-rest-6.0

        Args:
            project (Project): project instance. Can't be None
            expand (bool): A value indicating whether or not to expand Identity information in the result WebApiTeam object. Default: False
            current_user (bool): If true return all the teams requesting user is member, otherwise return all the teams user has read access. Default: False
            skip (int): Number of teams to skip. Default: 0
        
        Returns:
            List of teams: List[Team]
        
        Raises:
            ClientError if project is None or bad request
        '''

        if not project:
            raise ClientError('ProjectClient::get_project_teams: project can\'t be None')

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
                    teams += [Team.from_json(json_item) for json_item in json_items]
                    query_params['$skip'] = str(len(teams))
                else:
                    raise ClientError('ProjectClient::get_project_teams: response doesn\'t have \'value\' attribute')
            
            return teams
        except Exception as ex:
            raise ClientError(f'ProjectClient::get_project_teams: exception raised. Msg: {ex}', ex)

    def get_project_team_members(self, project: Project, team: Team) -> List[TeamMember]:
        '''
        Get a list of members for a specific team and a project.
        Docs: https://docs.microsoft.com/en-us/rest/api/azure/devops/core/teams/get-team-members-with-extended-properties?view=azure-devops-rest-6.0

        Args:
            project (Project): project instance of the team project the team belongs to.
            team (Team): team instance

        Returns:
            List of team members: List[TeamMember]
        
        Raises:
            ClientError if project or team is None
            ClientError if bad request

        '''
        
        if not project:
            raise ClientError('ProjectClient::get_project_team_members: project can\'t be None')
        
        if not team:
            raise ClientError('ProjectClient::get_project_team_members: team can\'t be None')

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
                    members += [TeamMember.from_json(json_item['identity']) for json_item in json_items]
                    query_params['$skip'] = str(len(members))
                else:
                    raise ClientError('ProjectClient::get_project_team_members: response doesn\'t have \'value\' attribute')

            return members
        except Exception as ex:
            raise ClientError(f'ProjectClient::get_project_team_members: exception raised. Msg: {ex}', ex)
