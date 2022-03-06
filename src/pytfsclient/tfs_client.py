from .http_client import HttpClient

API_VERSION = '6.0'
API_VERSION_PREVIEW = '6.0-preview.3'

def batch(iterable, n=1):
    """
    "batch" function that would take as input an iterable and return an iterable of iterables
    https://stackoverflow.com/a/8290508/6753144
    """
    len_ = len(iterable)
    for ndx in range(0, len_, n):
        yield iterable[ndx:min(ndx + n, len_)]

class TfsClientError(Exception):
    '''
    TfsClientError exception raised in API calls
    '''
    pass

class TfsBaseClient:
    def __init__(self, server_url: str, project_name: str='DefaultCollection', verify_ssl: bool=False) -> None:
        if not server_url.endswith('/'):
            server_url += '/'
        
        self.__server_url = server_url
        self._http_client = HttpClient(server_url, verify=verify_ssl)

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
        self.__collection = collection
        self.__project_name = project

        # API responce only in Project, without subproject
        self._url = '{}/_apis'.format(collection)
        self._url_prj = ('{}/{}/_apis'.format(collection, project)) if project else self.__url
    
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
    
    @property
    def api_url(self) -> str:
        """
        :return: TFS server api URL
        """
        return self._url

    @property
    def project_url(self) -> str:
        """
        :return: TFS server project api URL
        """
        return self._url_prj
    
    @project_name.setter
    def project_name(self, name: str) -> None:
        """
        :setter: sets TFS server project name and project api url
        """
        self.__project_name = name
        self._url_prj = ('{}/{}/_apis'.format(self.collection, name)) if name else self.__url
    
    @property
    def http_client(self) -> HttpClient:
        """
        :return: configured HTTP client
        """
        return self._http_client

    def authentificate_with_password(self, user_name: str, user_password: str) -> None:
        """
        Authorize with user name and password
        
        :param user_name (str): user name
        :param user_password (str): user password
        """
        self._http_client.authentificate_with_password(user_name, user_password)

    def authentificate_with_pat(self, personal_access_token: str) -> None:
        """
        Authorize with personal access token (PAT)

        :param personal_access_token (str): user personal access token
        """
        assert personal_access_token, 'TfsBaseClient::authentificate_with_pat: personal access token can\'t be None'

        self._http_client.authentificate_with_pat(personal_access_token)
    


    