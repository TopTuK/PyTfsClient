from ..client_error import ClientError

class Team:
    '''
    Team model class contains infromation about TFS/Azure team such as id, name and url
    '''

    @property
    def id(self) -> str:
        '''
        Returns:
            ID of TFS/Azure Team
        '''
        return self.__id

    @property
    def name(self) -> str:
        '''
        Returns:
            Name of TFS/Azure Team
        '''
        return self.__name

    @property
    def url(self) -> str:
        '''
        Returns:
            URL of TFS/Azure Team
        '''
        return self.__url

    @classmethod
    def create(cls, id: str, name: str, url: str = None):
        '''
        Classmethod creates instance of Team class.

        Args:
            id (str): ID of TFS team. Can\'t be None.
            name (str): name of TFS team. Can\'t be None.
            url (str): url for TFS team

        Returns:
            Instance of Team class

        Raises:
            ClientError: if id or name is None
        '''

        if not id:
            raise ClientError('Id can\'t be None')
        
        if not name:
            raise ClientError('Name can\'t be None')

        team = cls()

        team.__id = id
        team.__name = name
        team.__url = url

        return team

    @classmethod
    def from_json(cls, json_item):
        '''
        Classmethod creates instance of Team class from given json object

        Args:
            json_item (object): JSON object with 'id', 'name' and 'url' attributes.

        Returns:
            Instance of Team class
        '''

        team = cls()

        try:
            team.__id = json_item['id']
            team.__name = json_item['name']
            team.__url = json_item['url']
        except Exception as ex:
            raise ClientError(ex)

        return team