from enum import Enum

class RelationTypes(Enum):
    PARENT = 0
    CHILD = 1
    AFFECTS = 2
    AFFECTEDBY = 3
    RELATED = 4

RelationMap = {
    RelationTypes.PARENT : 'System.LinkTypes.Hierarchy-Reverse',
    RelationTypes.CHILD : 'System.LinkTypes.Hierarchy-Forward',
    RelationTypes.AFFECTS : 'Microsoft.VSTS.Common.Affects-Forward',
    RelationTypes.AFFECTEDBY : 'Microsoft.VSTS.Common.Affects-Reverse',
    RelationTypes.RELATED : 'System.LinkTypes.Related'
}

class TfsWorkitemRelation:
    """
    TFS relation model class.
    """
    __WORKITEM_SUBSTR = 'workItems/'
    __WORKITEM_SUBSTR_LENGTH = len(__WORKITEM_SUBSTR)

    @property
    def destination_id(self) -> int:
        """
        Id of destination workitem.
        """
        return self.__destination_id
    
    @property
    def url(self) -> str:
        """
        URL of destination workitem.
        """
        return self.__url
    
    @property
    def relation_name(self) -> str:
        """
        Relation type name.
        """
        return self.__relation_name

    #@staticmethod
    @classmethod
    def from_json(cls, json_item):
        """
        Creates TfsWorkitem instance from given json item instance.
        
        :return: TfsWorkitem instance.
        """
        #relation = TfsWorkitemRelation()
        relation = cls()

        url = json_item['url']
        relation.__url = url

        relation_name = json_item['rel']
        relation.__relation_name = relation_name

        def get_id():
            wi_id = None

            start_idx = url.find(TfsWorkitemRelation.__WORKITEM_SUBSTR)
            if start_idx > 1:
                start = int(start_idx + TfsWorkitemRelation.__WORKITEM_SUBSTR_LENGTH)
                wi_id = int(url[start:])

            return wi_id

        relation.__destination_id = get_id()

        return relation
    
    #@staticmethod
    @classmethod
    def create(cls, relation_name: str, workitem):
        """
        Creates relation for given relation type name and TfsWorkitem instance.
        
        :param: relation_name (str): relation type name. Can't be None.
        :param: workitem (TfsWorkitem): TfsWorkitem instance, Can't be None.
        :return: TfsWorkitem instance.
        """
        assert relation_name, 'TfsWorkitemRelation::create: relation name can\'t be None'
        assert workitem, 'TfsWorkitemRelation::create: workitem can\'t be None'

        relation = TfsWorkitemRelation()

        relation.__relation_name = relation_name
        relation.__url = workitem.url
        relation.__destination_id = workitem.id

        return relation