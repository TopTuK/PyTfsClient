from ..client_error import ClientError

class Project:
    '''
    Project model class contains information about ID, name and description of TFS/Azure Project.
    Use ProjectClient::get_projects() to get information about projects.
    '''

    @property
    def id(self) -> str:
        '''
        Returns:
            ID of TFS/Azure project
        '''
        return self.__id

    @property
    def name(self) -> str:
        '''
        Returns:
            Name of TFS/Azure project
        '''
        return self.__name
    
    @property
    def description(self) -> str:
        '''
        Returns:
            Description of TFS/Azure Project
        '''
        return self.__description

    @property
    def url(self) -> str:
        '''
        Returns:
            URL of TFS/Azure project
        '''
        return self.__url

    @classmethod
    def create(cls, id: str, name: str, description: str = None, url: str = None):
        '''
        Classmethod creates TFS/Azure project class instance.

        Args:
            id (str): ID of TFS/Azure project.
            name (str): name of TFS/Azure project.
            description (str): description of TFS/Azure project. Default: None
            url (str): url of TFS/Azure project. Default: None

        Returns:
            Instance of Project class

        Raises:
            ClientError: if id or name is None
        '''

        if not id:
            raise ClientError('Id can\'t be None')
        
        if not name:
            raise ClientError('Name can\'t be None')

        team_project = cls()

        team_project.__id = id
        team_project.__name = name
        team_project.__description = description
        team_project.__url = url

        return team_project

    @classmethod
    def from_json(cls, json_item):
        '''
        Classmethod creates TFS/Azur project class instance from given JSON object
        
        Args:
            json_item (object): JSON object with 'id', 'name' and 'url' attributes. 'description' attribute can be None

        Returns:
            Instance of Project class
        '''
        team_project = cls()

        try:
            team_project.__id = json_item['id']
            team_project.__name = json_item['name']
            team_project.__description = json_item['description'] if 'description' in json_item else None
            team_project.__url = json_item['url']
        except Exception as ex:
            raise ClientError(ex)
        
        return team_project