class TfsProject:
    """
    TFS project model class
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
    def url(self) -> str:
        """
        URL of TFS project
        """
        return self.__url

    @classmethod
    def create(cls, id: str, name: str, url: str = None):
        """
        Create TFS project instance.

        :param: id (str): ID of TFS project. Can\'t be None.
        :param: name (str): name of TFS project. Can't be None.
        :param: url (str): url of TFS project.
        :return: TfsProject instance.
        """
        assert id, 'TfsProject::create: id can\'t be None'
        assert name, 'TfsProject::create: name can\'t be None'

        team_project = cls()

        team_project.__id = id
        team_project.__name = name
        team_project.__url = url

        return team_project

    @classmethod
    def from_json(cls, json_item):
        """
        Create TFS project object from given json object

        :return: (TfsProject) object
        """
        team_project = cls()
        #team_project = TfsProject()

        team_project.__id = json_item['id']
        team_project.__name = json_item['name']
        team_project.__url = json_item['url']
        
        return team_project

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
        assert id, 'TfsTeam::create: id can\'t be None'
        assert name, 'TfsTeam::create: name can\'t be None'

        team = cls()

        team.__id = id
        team.__name = name
        team.__url = url

        return team

    #@staticmethod
    @classmethod
    def from_json(cls, json_item):
        """
        Creates TfsTeam object from given json object
        """
        #team = TfsTeam()
        team = cls()

        team.__id = json_item['id']
        team.__name = json_item['name']
        team.__url = json_item['url']

        return team

class TeamMember:
    """
    TFS team member model class
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
        assert id, 'TeamMember::create: id can\'t be None'
        assert display_name, 'TeamMember::create: display_name can\'t be None'
        assert unique_name, 'TeamMember::create: unique_name can\'t be None'

        member = cls()

        member.__id = id
        member.__display_name = display_name
        member.__unique_name = unique_name
        member.__url = url

        return member

    #@staticmethod
    @classmethod
    def from_json(cls, json_item):
        """
        Creates TfsTeamMember from given json object
        """
        #member = TeamMember()
        member = cls()

        member.__id = json_item['id']
        member.__display_name = json_item['displayName']
        member.__unique_name = json_item['uniqueName']
        member.__url = json_item['url']

        return member