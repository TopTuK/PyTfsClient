from enum import Enum
from ..client_error import ClientError

class RelationTypes(Enum):
    '''
    ENUM: Common relation types.
    '''

    PARENT = 0
    CHILD = 1
    AFFECTS = 2
    AFFECTEDBY = 3
    RELATED = 4

'''
Relations MAP dictonary. Key: RelationTypes, Value: str.
    RelationTypes.PARENT : 'System.LinkTypes.Hierarchy-Reverse',
    RelationTypes.CHILD : 'System.LinkTypes.Hierarchy-Forward',
    RelationTypes.AFFECTS : 'Microsoft.VSTS.Common.Affects-Forward',
    RelationTypes.AFFECTEDBY : 'Microsoft.VSTS.Common.Affects-Reverse',
    RelationTypes.RELATED : 'System.LinkTypes.Related'
'''
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
    '''
    WorkitemRelation class contains information about relation between workitems.
    '''

    ### Properties region ###

    @property
    def destination_id(self) -> int:
        '''
        Returns:
            Id of destination workitem of relation.
        '''

        return self.__destination_id
    
    @property
    def url(self) -> str:
        '''
        Returns:
            URL of relation.
        '''

        return self.__url
    
    @property
    def relation_name(self) -> str:
        '''
        Returns:
            Relation type name.
        '''

        return self.__relation_name
    
    ### END OF PROPERTIES REGION ###

    @classmethod
    def from_json(cls, json_item):
        '''
        Classmethod creates WorkitemRelation class instance from given json object
        
        Args:
            json_item (object): json response from TFS Server contains information about workitem relation.

        Returns:
            WorkitemRelation class instance
        
        Raises:
            ClientError if json_item is invalid
        '''
        
        relation = cls()

        try:
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
        except Exception as ex:
            raise ClientError(ex)
    
    @classmethod
    def create(cls, relation_name: str, workitem):
        '''
        Classmethod Creates relation of given relation type name and workitem instance.
        
        Args:
            relation_name (str): relation type name.
            workitem (Workitem): instance of workitem.

        Returns:
            WorkitemRelation class instance

        Raises:
            ClientError: if relation name or workitem instance is None
        '''

        if not relation_name:
            raise ClientError('Relation name can\'t be None')
        

        if not workitem:
            raise ClientError('Workitem can\'t be None')

        relation = WorkitemRelation()

        relation.__relation_name = relation_name
        relation.__url = workitem.url
        relation.__destination_id = workitem.id

        return relation