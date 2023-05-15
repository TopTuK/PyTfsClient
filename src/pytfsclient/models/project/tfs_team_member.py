from ..client_error import ClientError

class TeamMember:
    '''
    TeamMember model class contains information about project team member.
    Use ProjectClient::get_project_team_members() or ProjectClient::get_project_team_members to get information about team members.
    '''

    @property
    def id(self) -> str:
        '''
        Returns:
            ID of TFS/Azure team member
        '''
        return self.__id
    
    @property
    def display_name(self) -> str:
        '''
        Returns:
            Displaing name of TFS/Azure team member
        '''
        return self.__display_name
    
    @property
    def unique_name(self) -> str:
        '''
        Returns:
            Unique name (e.g. email) of TFS/Azure team member
        '''
        return self.__unique_name
    
    @property
    def url(self) -> str:
        '''
        Returns:
            URL of TFS/Azure team member
        '''
        return self.__url
    
    def __str__(self):
        '''
        Returns:
            display_name: str
        '''
        return self.display_name
    
    def __repr__(self):
        '''
        Returns:
            display_name: str
        '''
        return self.display_name

    @classmethod
    def create(cls, id: str, display_name: str, unique_name: str, url: str = None):
        '''
        Classmethod creates TeamMember class instance

        Args:
            id (str): ID of TFS/Azure team member.
            display_name (str): display name of TFS/Azure team member.
            unique_name (str): unique name of TFS/Azure team member.
            url (str): url of TFS/Azure team member. Default: None

        Returns:
            Instance of TeamMember class

        Raises:
            ClientError: if id or display_name or unique_name is None
        '''

        if not id:
            raise ClientError('Id can\'t be None')
        
        if not display_name:
            raise ClientError('display_name can\'t be None')
        
        if not unique_name:
            raise ClientError('unique_name can\'t be None')

        member = cls()

        member.__id = id
        member.__display_name = display_name
        member.__unique_name = unique_name
        member.__url = url

        return member

    @classmethod
    def from_json(cls, json_item):
        '''
        Classmethod creates TeamMember class instance from given json object

        Args:
            json_item (object): JSON object with 'id', 'displayName', 'uniqueName' and 'url' attributes. 'description' attribute can be None

        Returns:
            Instance of TeamMember class
        '''
        member = cls()

        try:
            member.__id = json_item['id'] if 'id' in json_item else None
            member.__display_name = json_item['displayName'] if 'displayName' in json_item else 'Unknown user'
            member.__unique_name = json_item['uniqueName'] if 'uniqueName' in json_item else member.__display_name
            member.__url = json_item['url'] if 'url' in json_item else None
        except Exception as ex:
            raise ClientError(ex)

        return member