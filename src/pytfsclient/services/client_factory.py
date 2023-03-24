from pytfsclient.services.client_connection import ClientConnection
from pytfsclient.services.http.http_client import HttpClient
from pytfsclient.services.mention_client.mention_client import MentionClient
from pytfsclient.services.project_client.project_client import ProjectClient
from pytfsclient.services.workitem_client.workitem_client import WorkitemClient

class ClientFactory:
    """
    Static ClientFactory class with static functions helps to create TFS clients for different purposes.
    It is main entry point to PyTfsClient library.

    The main functions are create_ntlm(), create_pat(). They returns instanse of Client Connection class.

    Functions:
    - get_project_client() -> returns ProjectClient facade for managing projects, teams and team members.
    - get_workitem_client() -> returns WorkitemClient facade for managing workitems and relations.
    """

    @staticmethod
    def create_ntlm(user_name: str, user_password: str, server_url: str, project_name: str='DefaultCollection', verify_ssl: bool=False) -> ClientConnection:
        """
        """

        assert user_name, 'User name can\'t be None'
        assert user_password, 'User password can\'t be None'
        assert server_url, 'Server URL can\'t be None'

        http_client = HttpClient(server_url, verify_ssl)
        http_client.authentificate_with_password(user_name, user_password)

        return ClientConnection(http_client, project_name)

    @staticmethod
    def create_pat(personal_access_token: str, server_url: str, project_name: str='DefaultCollection', verify_ssl: bool=False) -> ClientConnection:
        """
        """

        assert personal_access_token, 'Personal access token can\'t be None'
        assert server_url, 'Server URL can\'t be None'

        http_client = HttpClient(server_url, verify_ssl)
        http_client.authentificate_with_pat(personal_access_token)
        
        return ClientConnection(http_client, project_name)

    @staticmethod
    def create_http_client(http_client: HttpClient, project_name: str='DefaultCollection') -> ClientConnection:
        """
        """

        assert http_client, 'HTTP Client can\'t be None'
        
        return ClientConnection(http_client, project_name)
    
    @staticmethod
    def get_workitem_client(client_connection: ClientConnection) -> WorkitemClient:
        """
        Returns Tfs WorkitemClient facade for managing workitems and relations
        """

        assert client_connection, 'Client Connection can\'t be None'

        return WorkitemClient(client_connection)
    
    @staticmethod
    def get_project_client(client_connection: ClientConnection) -> ProjectClient:
        """
        Returns Tfs ProjectClient facade for managing projects, teams and team members
        """

        assert client_connection, 'Client Connection can\'t be None'
        
        return ProjectClient(client_connection)
    
    @staticmethod
    def get_mention_client() -> MentionClient:
        """
        Return TFS MentionClient facade for mention users in workitems.
        """

        return MentionClient()
