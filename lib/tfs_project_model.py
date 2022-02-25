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
        Dispang name of TFS team member
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