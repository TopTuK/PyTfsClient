from .services.http.http_client import HttpClient
from .client_connection import ClientConnection
from .services.mention_client.mention_client import MentionClient
from .services.project_client.project_client import ProjectClient
from .services.workitem_client.workitem_client import WorkitemClient
from .models.client_error import ClientError

class ClientFactory:
    '''
    Main factory of PyTfsClient library (entry point). Used to get an instance of a Client Connection.
    The main functions are create_ntlm() or create_pat(). They returns instanse of ClientConnection.

    Functions to get facades:
    - get_project_client() -> returns ProjectClient facade for managing projects, teams and team members.
    - get_workitem_client() -> returns WorkitemClient facade for managing workitems.
    '''

    @staticmethod
    def create_ntlm(user_name: str, user_password: str, server_url: str, project_name: str='DefaultCollection', verify_ssl: bool=False) -> ClientConnection:
        '''
        Creates ClientConnection instance with NTLM authorization for connection to TFS/Azure.

        Args:
            For NTLM authorization:
                user_name (str): user name
                user_password (str): user password

            server_url (str): URL of TFS/Azure service
            project_name (str): project name with collection. Default is 'DefaultCollection' without project
            verify_ssl (bool): flag for verifing SSL. Default is False

        Returns:
            Instance of ClientConnection with NTLM authorization for connection to TFS/Azure

        Raises:
            ConnectionError: if user_name, user_password or server_url are None
        '''

        if not user_name:
            raise ClientError('User name can\'t be None')
        
        if not user_password:
            raise ClientError('User password can\'t be None')
        
        if not server_url:
            raise ClientError('Server URL can\'t be None')

        http_client = HttpClient(server_url, verify_ssl)
        http_client.authentificate_with_password(user_name, user_password)

        return ClientConnection(http_client, project_name)

    @staticmethod
    def create_pat(personal_access_token: str, server_url: str, project_name: str='DefaultCollection', verify_ssl: bool=False) -> ClientConnection:
        '''
        Creates ClientConnection instance with authorization with personal access token for connection to TFS/Azure.
        
        Args:
            personal_access_token (str): personal access token for connection to TFS/Azure service

            server_url (str): URL of TFS/Azure service
            project_name (str): project name with collection. Default is 'DefaultCollection' without project
            verify_ssl (bool): flag for verifing SSL. Default is False

        Returns:
            Instance of ClientConnection with NTLM authorization for connection to TFS/Azure

        Raises:
            ConnectionError: if personal_access_token or server_url are None
        '''

        if not personal_access_token:
            raise ClientError('Personal access token can\'t be None')
        
        if not server_url:
            raise ClientError('Server URL can\'t be None')

        http_client = HttpClient(server_url, verify_ssl)
        http_client.authentificate_with_pat(personal_access_token)
        
        return ClientConnection(http_client, project_name)

    @staticmethod
    def create_http_client(http_client: HttpClient, project_name: str='DefaultCollection') -> ClientConnection:
        '''
        Creates ClientConnection instance with given instance of HttpClient for connection to TFS/Azure.
        Used for custom authorization realization.

        Args:
            http_client (HttpClient): instance of HttpClient with custom authorization
            project_name (str): project name with collection. Default is 'DefaultCollection' without project

        Returns:
            Instance of ClientConnection with custom authorization for connection to TFS/Azure

        Raises:
            ConnectionError: if http_client is None
        '''

        if not http_client:
            raise ClientError('HTTP Client can\'t be None')
        
        return ClientConnection(http_client, project_name)
    
    @staticmethod
    def get_workitem_client(client_connection: ClientConnection) -> WorkitemClient:
        '''
        Returns instance of WorkitemClient facade for managing workitems.

        Args:
            client_connection (ClientConnection): instance of ClientConnection with defined authorization

        Returns:
            Instance of WorkitemClient facade for managing workitems TFS/Azure service.

        Raises:
            ConnectionError: if client_connection is None
        '''

        if not client_connection:
            raise ClientError('Client Connection can\'t be None')

        return WorkitemClient(client_connection)
    
    @staticmethod
    def get_project_client(client_connection: ClientConnection) -> ProjectClient:
        '''
        Returns instance of ProjectClient facade for managing projects, teams and members of TFS/Azure service.

        Args:
            client_connection (ClientConnection): instance of ClientConnection with defined authorization

        Returns:
            Instance of ProjectClient facade for managing projects, teams and members of TFS/Azure service.

        Raises:
            ConnectionError: if client_connection is None
        '''

        if not client_connection:
            raise ClientError('Client Connection can\'t be None')
        
        return ProjectClient(client_connection)
    
    @staticmethod
    def get_mention_client() -> MentionClient:
        '''
        Returns:
            Instance of MentionClient facade for mention users in workitems.
        '''

        return MentionClient()
