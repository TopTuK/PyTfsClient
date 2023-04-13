from .services.http.http_client import HttpClient
from .models.client_error import ClientError

class ClientConnection:
    '''
    ClientConnection class contains information about connecting to the TFS/Azure service.
    '''
    
    # Constructor
    def __init__(self, http_client: HttpClient, project_name: str='DefaultCollection') -> None:
        '''
        ClientConnection constructor. Creates instance of ClientConnection class

        Args:
            http_client: instance of HttpClient
            project_name: name of Tfs/Azure project. Default is 'DefaultCollection

        Returns:
            Instance of ClientConnection

        Raises:
            ConnectionError: if http_client or project_name is None
        '''

        if not http_client:
            raise ClientError('http_client is None')

        if not project_name:
            raise ClientError('project_name is None')

        server_url = http_client.base_url

        if not server_url.endswith('/'):
            server_url += '/'
        
        self.__server_url = server_url
        self.__http_client = http_client

        # Closure function to get collection and project from project name
        # Remove part after / in project_name, like DefaultCollection/MyProject => DefaultCollection
        def get_collection_and_project():
            splitted_project = project_name.split('/')
            collection = splitted_project[0]
            project = None

            if len(splitted_project) > 1:
                project = splitted_project[1]
                # If not space
                if project:
                    project = project.split('/')[0]

            return collection, project
        
        collection, project = get_collection_and_project()

        # Assign Collection and Project
        self.__collection = collection
        self.__project_name = project

    ### Properties section ###

    @property
    def server_url(self) -> str:
        '''
        Returns TFS/Azure server URL
        '''
        return self.__server_url
    
    @property
    def collection(self) -> str:
        '''
        Returns TFS/Azure collection name.
        if you set project name as DefaultCollection/MyProject this property return DefaultCollection.
        '''
        return self.__collection

    @property
    def project_name(self) -> str:
        '''
        Returns TFS/Azure project name.
        if you set project name as DefaultCollection/MyProject this property return MyProject.
        '''
        return self.__project_name
    
    @project_name.setter
    def project_name(self, name: str) -> None:
        '''
        Sets project name for current connection.
        '''
        self.__project_name = name
    
    @property
    def http_client(self) -> HttpClient:
        '''
        Returns instance of HttpClient with defined authorization
        '''
        return self.__http_client
     
    @property
    def api_url(self) -> str:
        '''
        Returns TFS/Azure API part of URL (collection without project). Ends with '/'.
        '''
        return f'{self.__collection}/_apis/'

    # API response only for Collection/Project
    @property
    def project_url(self) -> str:
        '''
        Returns TFS/Azure project API part of URL. Ends with '/'.
        '''
        return f'{self.__collection}/{self.__project_name}/_apis/' if self.__project_name else self.api_url