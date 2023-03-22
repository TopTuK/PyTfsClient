class TfsTeam:
    """
    TFS Team model class
    """

    @property
    def id(self) -> str:
        """
        ID of TFS Team
        """
        return self.__id

    @property
    def name(self) -> str:
        """
        Name of TFS Team
        """
        return self.__name

    @property
    def url(self) -> str:
        """
        URL of TFS Team
        """
        return self.__url

    @classmethod
    def create(cls, id: str, name: str, url: str = None):
        """
        Creates TFSTeam instance.

        :param: id (str): ID of TFS team. Can\'t be None.
        :param: name (str): name of TFS team. Can\'t be None.
        :param: url (str): url for TFS team
        :return: TFSTeam instance.
        """
        assert id, 'Id can\'t be None'
        assert name, 'Name can\'t be None'

        team = cls()

        team.__id = id
        team.__name = name
        team.__url = url

        return team

    @classmethod
    def from_json(cls, json_item):
        """
        Creates TfsTeam object from given json object
        """
        team = cls()

        team.__id = json_item['id']
        team.__name = json_item['name']
        team.__url = json_item['url']

        return team