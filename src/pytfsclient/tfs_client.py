from .client_connection import ClientConnection

class TfsClientError(Exception):
    '''
    TfsClientError exception raised in API calls
    '''
    pass

class TfsBaseClient:
    def __init__(self, client_connection: ClientConnection) -> None:
        assert client_connection, 'Client connection is None'

        self.__client_connection = client_connection

        self._url = client_connection.api_url
        self._url_prj = client_connection.project_url

    @property
    def client_connection(self) -> ClientConnection:
        return self.__client_connection
    
    @property
    def server_url(self) -> str:
        """
        :return: TFS server URL (str)
        """
        return self.__client_connection.server_url

    @property
    def collection(self) -> str:
        """
        :return: current TFS collection
        """
        return self.__client_connection.collection

    @property
    def project_name(self) -> str:
        """
        :return: current TFS project name
        """
        return self.__client_connection.project_name
    
    @property
    def api_url(self) -> str:
        """
        :return: TFS server api URL
        """
        return self.__client_connection.api_url

    @property
    def project_url(self) -> str:
        """
        :return: TFS server project api URL
        """
        return self.__client_connection.project_url
    
    @project_name.setter
    def project_name(self, name: str) -> None:
        """
        :setter: sets TFS server project name and project api url
        """

        self.__client_connection.project_name = name
    
    @property
    def http_client(self):
        """
        :return: configured HTTP client
        """
        return self.__client_connection.http_client

    def authentificate_with_password(self, user_name: str, user_password: str) -> None:
        """
        Authorize with user name and password
        
        :param user_name (str): user name
        :param user_password (str): user password
        """
        self.__client_connection.http_client.authentificate_with_password(user_name, user_password)

    def authentificate_with_pat(self, personal_access_token: str) -> None:
        """
        Authorize with personal access token (PAT)

        :param personal_access_token (str): user personal access token
        """
        assert personal_access_token, 'TfsBaseClient::authentificate_with_pat: personal access token can\'t be None'

        self.__client_connection.http_client.authentificate_with_pat(personal_access_token)
    


    