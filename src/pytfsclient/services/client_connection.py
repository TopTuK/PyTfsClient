from .http.http_client import HttpClient

class ClientConnection:
    """
    """
    
    # Constructor
    def __init__(self, http_client: HttpClient, project_name: str='DefaultCollection') -> None:
        server_url = http_client.base_url

        if not server_url.endswith('/'):
            server_url += '/'
        
        self.__server_url = server_url
        self.__http_client = http_client

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
        
        # Remove part after / in project_name, like DefaultCollection/MyProject => DefaultCollection
        collection, project = get_collection_and_project()

        # Assign Collection and Project
        self.__collection = collection
        self.__project_name = project

    ### Properties section ###

    @property
    def server_url(self) -> str:
        """
        :return: TFS server URL (str)
        """
        return self.__server_url
    
    @property
    def collection(self) -> str:
        """
        :return: current TFS collection
        """
        return self.__collection

    @property
    def project_name(self) -> str:
        """
        :return: current TFS project name
        """
        return self.__project_name
    
    @project_name.setter
    def project_name(self, name: str) -> None:
        """
        :setter: sets TFS server project name and project api url
        """
        self.__project_name = name
    
    @property
    def http_client(self) -> HttpClient:
        """
        :return: configured HTTP client
        """
        return self.__http_client
    
    # Remove part after / in project-name, like DefaultCollection/MyProject => DefaultCollection
    # API responce only in Project, without subproject    
    @property
    def api_url(self) -> str:
        """
        :return: TFS server api URL ending with '/'
        """
        return f'{self.__collection}/_apis/'

    # API response only for Collection/Project
    @property
    def project_url(self) -> str:
        """
        :return: TFS server project api URL ending with '/'
        """
        return f'{self.__collection}/{self.__project_name}/_apis/' if self.__project_name else self.api_url