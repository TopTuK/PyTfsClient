from .tfs_client import TfsBaseClient
from .tfs_project_client import TfsProjectClient
from .tfs_workitem_client import TfsWorkitemClient

class TfsClientFactory:
    """
    TfsClientFactory class with static functions helps to create TFS clients for different purposes.
    It is main entry point to PyTfsClient library.

    The main function is TfsClientFactory::create() -> return TfsBaseClient
    Functions:
    - get_project_client() -> return TfsProjectClient facade for managing projects, teams and team members
    - get_workitem_client() -> return TfsWorkitemClient facade for managing workitems and relations
    """

    @staticmethod
    def create(server_url: str, project_name: str='DefaultCollection', verify_ssl: bool=False) -> TfsBaseClient:
        """
        create() function provides TfsBaseClient. It is main entry point to library
        TfsBaseClient provides authorization methods and helper properties for making API calls.

        Sample usage:
        client = TfsClientFactory.create('https://tfs-server/tfs', 'DefaultCollection/Tfs project')
        client.authentificate_with_password('username', 'userpassword')

        :param server_url (str): TFS server url address. Can't be None
        :param project_name (str): default collection and project names. Separator symbol is '/'. Eg: DefaultCollection/Tfs project -> (collection: DefaultCollection, project: Tfs project)
        :param verify_ssl (bool): if True raises exception if detects SSL problems
        :return: (TfsBaseClient) client with information about collection and project.
        """
        assert server_url, 'Server url can\'t be None'

        client = TfsBaseClient(server_url=server_url, project_name=project_name, verify_ssl=verify_ssl)

        return client
    
    @staticmethod
    def get_project_client(client: TfsBaseClient) -> TfsProjectClient:
        """
        Returns TfsProjectClient facade for managing projects, teams and team members

        :param client (TfsBaseClient): configured TFS client object. Can't be None
        :return: TfsProjectClient facade object
        """
        assert client, 'client can\'t be None'

        return TfsProjectClient(client=client)

    @staticmethod
    def get_workitem_client(client: TfsBaseClient) -> TfsWorkitemClient:
        """
        Returns TfsWorkitemClient facade for managing workitems and relations

        :param client (TfsBaseClient): configured TFS client object. Can't be None
        :return: TfsWorkitemClient facade object
        """
        assert client, 'client can\'t be None'

        return TfsWorkitemClient(client=client)