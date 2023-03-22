class TfsTeamMemeber:
    """
    TFS Team Member model class
    """

    @property
    def id(self) -> str:
        """
        ID of TFS team member
        """
        return self.__id
    
    @property
    def display_name(self) -> str:
        """
        Displaing name of TFS team member
        """
        return self.__display_name
    
    @property
    def unique_name(self) -> str:
        """
        Unique name (e.g. email) of TFS team member
        """
        return self.__unique_name
    
    @property
    def url(self) -> str:
        """
        URL of TFS team member
        """
        return self.__url

    @classmethod
    def create(cls, id: str, display_name: str, unique_name: str, url: str = None):
        """
        """
        assert id, 'Id can\'t be None'
        assert display_name, 'Display_name can\'t be None'
        assert unique_name, 'Unique_name can\'t be None'

        member = cls()

        member.__id = id
        member.__display_name = display_name
        member.__unique_name = unique_name
        member.__url = url

        return member

    @classmethod
    def from_json(cls, json_item):
        """
        Creates TfsTeamMember from given json object
        """
        member = cls()

        member.__id = json_item['id']
        member.__display_name = json_item['displayName']
        member.__unique_name = json_item['uniqueName']
        member.__url = json_item['url']

        return member