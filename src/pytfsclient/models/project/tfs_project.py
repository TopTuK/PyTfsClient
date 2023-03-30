class TfsProject:
    """
    TFS Project model class
    """

    @property
    def id(self) -> str:
        """
        ID of TFS project
        """
        return self.__id

    @property
    def name(self) -> str:
        """
        Name of TFS project
        """
        return self.__name
    
    @property
    def description(self) -> str:
        """
        Description of TFS Project
        """
        return self.__description

    @property
    def url(self) -> str:
        """
        URL of TFS project
        """
        return self.__url

    @classmethod
    def create(cls, id: str, name: str, description: str = None, url: str = None):
        """
        Create TFS project instance.
        """
        assert id, 'Id can\'t be None'
        assert name, 'Name can\'t be None'

        team_project = cls()

        team_project.__id = id
        team_project.__name = name
        team_project.__description = description
        team_project.__url = url

        return team_project

    @classmethod
    def from_json(cls, json_item):
        """
        Create TFS project object from given JSON object
        :return: TfsProject instance
        """
        team_project = cls()

        team_project.__id = json_item['id']
        team_project.__name = json_item['name']
        team_project.__description = json_item['description'] if 'description' in json_item else None
        team_project.__url = json_item['url']
        
        return team_project