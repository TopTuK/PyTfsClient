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

_WORKITEM_SUBSTR = 'workItems/'
_WORKITEM_SUBSTR_LENGTH = len(_WORKITEM_SUBSTR)

class WorkitemRelation:
    """
    TFS relation model class.
    """

    ### Properties region ###

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
    
    ### END OF PROPERTIES REGION ###

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

        # Get workitem ID closure
        def get_id():
            wi_id = None

            start_idx = url.find(_WORKITEM_SUBSTR)
            if start_idx > 1:
                start = int(start_idx + _WORKITEM_SUBSTR_LENGTH)
                wi_id = int(url[start:])

            return wi_id

        relation.__destination_id = get_id()

        return relation
    
    @classmethod
    def create(cls, relation_name: str, workitem):
        """
        Creates relation for given relation type name and Tfs Workitem instance.
        """
        assert relation_name, 'Relation name can\'t be None'
        assert workitem, 'Workitem can\'t be None'

        relation = WorkitemRelation()

        relation.__relation_name = relation_name
        relation.__url = workitem.url
        relation.__destination_id = workitem.id

        return relation